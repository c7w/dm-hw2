import os
import logging
import numpy as np
import torch
torch.set_num_threads(2)
from torch.utils.data.dataset import random_split
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter
import torch.multiprocessing as mp
import torch.distributed as dist
from sklearn.model_selection import KFold, train_test_split
from collections import defaultdict

from rrl.utils import read_csv, DBEncoder
from rrl.models import RRL

DATA_DIR = './dataset'


def get_data_loader(dataset, world_size, rank, batch_size, k=0, pin_memory=False, save_best=True):
    if dataset in ["tic-tac-toe", "bank-marketing", "housing"]:
        data_path = os.path.join(DATA_DIR, dataset + '.data')
        info_path = os.path.join(DATA_DIR, dataset + '.info')
        X_df, y_df, f_df, label_pos = read_csv(data_path, info_path, shuffle=True)
        # import IPython; IPython.embed()

        db_enc = DBEncoder(f_df, discrete=False, is_regression=dataset == "housing",)
        db_enc.fit(X_df, y_df)

        X, y = db_enc.transform(X_df, y_df, normalized=True, keep_stat=True)

        kf = KFold(n_splits=5, shuffle=True, random_state=0)
        train_index, test_index = list(kf.split(X_df))[k]
        X_train = X[train_index]
        y_train = y[train_index]
        X_test = X[test_index]
        y_test = y[test_index]

        train_set = TensorDataset(torch.tensor(X_train.astype(np.float32)), torch.tensor(y_train.astype(np.float32)))
        test_set = TensorDataset(torch.tensor(X_test.astype(np.float32)), torch.tensor(y_test.astype(np.float32)))

        train_len = int(len(train_set) * 0.95)
        train_sub, valid_set = random_split(train_set, [train_len, len(train_set) - train_len])

        if save_best:  # use validation set for model selections.
            train_set = train_sub

        train_sampler = torch.utils.data.distributed.DistributedSampler(train_set, num_replicas=world_size, rank=rank)

        train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=False, pin_memory=pin_memory, sampler=train_sampler)
        valid_loader = DataLoader(valid_set, batch_size=batch_size, shuffle=False, pin_memory=pin_memory)
        test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, pin_memory=pin_memory)

        return db_enc, train_loader, valid_loader, test_loader


    # elif dataset == "bank-marketing":
    #     from ucimlrepo import fetch_ucirepo

    #     bank_marketing = fetch_ucirepo(id=222)
    #     X_df = bank_marketing.data.features
    #     y_df = bank_marketing.data.targets
        
    #     # concat X and y
    #     import pandas as pd
    #     D = pd.concat([X_df, y_df], axis=1)

        
    #     # "age";"job";"marital";"education";"default";"balance";"housing";"loan";"contact";"day";"month";"duration";"campaign";"pdays";"previous";"poutcome";"y"
    #     numerical_cols = ["age", "balance", "duration", "campaign", "pdays", "previous"]
    #     from sklearn.preprocessing import MinMaxScaler
    #     scaler = MinMaxScaler()
    #     D[numerical_cols] = scaler.fit_transform(D[numerical_cols])
        
    #     yn_cols = ["default", "housing", "loan", "y"]
    #     for col in yn_cols:
    #         D[col] = D[col].map({"yes": 1, "no": 0})
        
    #     categorical_cols = ["job", "marital", "education", "contact", "month", "poutcome"]
    #     D = pd.get_dummies(D, columns=categorical_cols)
        
    #     # rearrange values. 
        
    #     X = D.drop(columns=["y"]).values
    #     y = D["y"].values
        
        
    #     kf = KFold(n_splits=5, shuffle=True, random_state=0)
    #     train_index, test_index = list(kf.split(X_df))[k]
    #     X_train = X[train_index]
    #     y_train = y[train_index]
    #     X_test = X[test_index]
    #     y_test = y[test_index]

    #     train_set = TensorDataset(torch.tensor(X_train.astype(np.float32)), torch.tensor(y_train.astype(np.float32)))
    #     test_set = TensorDataset(torch.tensor(X_test.astype(np.float32)), torch.tensor(y_test.astype(np.float32)))

    #     train_len = int(len(train_set) * 0.95)
    #     train_sub, valid_set = random_split(train_set, [train_len, len(train_set) - train_len])

    #     if save_best:  # use validation set for model selections.
    #         train_set = train_sub

    #     train_sampler = torch.utils.data.distributed.DistributedSampler(train_set, num_replicas=world_size, rank=rank)

    #     train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=False, pin_memory=pin_memory, sampler=train_sampler)
    #     valid_loader = DataLoader(valid_set, batch_size=batch_size, shuffle=False, pin_memory=pin_memory)
    #     test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, pin_memory=pin_memory)

    #     import IPython; IPython.embed()
    #     db_enc = DBEncoder(None)
    #     # used variables
    #     # X_fname = db_enc.X_fname
    #     # y_fname = db_enc.y_fname
    #     # discrete_flen = db_enc.discrete_flen
    #     # continuous_flen = db_enc.continuous_flen
        
    #     db_enc.X_fname = list(D.drop(columns=["y"]).columns)
    #     db_enc.y_fname = ["y"]
    #     db_enc.discrete_flen = 0
    #     db_enc.continuous_flen = len(db_enc.X_fname)

    #     return db_enc, train_loader, valid_loader, test_loader
        
        
        # import IPython; IPython.embed()

        
        
    else:
        raise ValueError('Unknown dataset: {}'.format(dataset))

def train_model(gpu, args):
    # rank = args.nr * args.gpus + gpu
    rank = 0
    # dist.init_process_group(backend='nccl', init_method='env://', world_size=args.world_size, rank=rank)
    torch.manual_seed(42)
    device_id = args.device_ids[gpu]
    torch.cuda.set_device(device_id)

    # if gpu == 0:
    writer = SummaryWriter(args.folder_path)
    is_rank0 = True
    # else:
    #     writer = None
    #     is_rank0 = False

    dataset = args.data_set
    db_enc, train_loader, valid_loader, _ = get_data_loader(dataset, args.world_size, rank, args.batch_size,
                                                            k=args.ith_kfold, pin_memory=True, save_best=args.save_best)

    X_fname = db_enc.X_fname
    y_fname = db_enc.y_fname
    discrete_flen = db_enc.discrete_flen
    continuous_flen = db_enc.continuous_flen

    rrl = RRL(dim_list=[(discrete_flen, continuous_flen)] + list(map(int, args.structure.split('@'))) + [len(y_fname)],
              device_id=device_id,
              use_not=args.use_not,
              is_rank0=is_rank0,
              log_file=args.log,
              writer=writer,
              save_best=args.save_best,
              estimated_grad=args.estimated_grad,
              use_skip=args.skip,
              save_path=args.model,
              use_nlaf=args.nlaf,
              alpha=args.alpha,
              beta=args.beta,
              gamma=args.gamma,
              temperature=args.temp, 
              is_regression=dataset == "housing",
              db_enc=db_enc,
              distributed=False)

    rrl.train_model(
        data_loader=train_loader,
        valid_loader=valid_loader,
        lr=args.learning_rate,
        epoch=args.epoch,
        lr_decay_rate=args.lr_decay_rate,
        lr_decay_epoch=args.lr_decay_epoch,
        weight_decay=args.weight_decay,
        log_iter=args.log_iter)


def load_model(path, device_id, log_file=None, distributed=True, db_enc=None, dataset="housing"):
    checkpoint = torch.load(path, map_location='cpu')
    saved_args = checkpoint['rrl_args']
    rrl = RRL(
        dim_list=saved_args['dim_list'],
        device_id=device_id,
        is_rank0=True,
        use_not=saved_args['use_not'],
        log_file=log_file,
        distributed=distributed,
        estimated_grad=saved_args['estimated_grad'],
        use_skip=saved_args['use_skip'],
        use_nlaf=saved_args['use_nlaf'],
        alpha=saved_args['alpha'],
        beta=saved_args['beta'],
        gamma=saved_args['gamma'],
        is_regression=dataset == "housing",
        db_enc=db_enc,)

    stat_dict = checkpoint['model_state_dict']
    for key in list(stat_dict.keys()):
        # remove 'module.' prefix
        if 'module.' in key:
            stat_dict[key[7:]] = stat_dict.pop(key)
    rrl.net.load_state_dict(checkpoint['model_state_dict'])
    return rrl


def test_model(args):
    dataset = args.data_set
    db_enc, train_loader, _, test_loader = get_data_loader(dataset, 4, 0, args.batch_size, args.ith_kfold, save_best=False,)
    rrl = load_model(args.model, args.device_ids[0], log_file=args.test_res, distributed=False, db_enc=db_enc, dataset=dataset)
    rrl.test(test_loader=test_loader, set_name='Test')
    if args.print_rule:
        with open(args.rrl_file, 'w') as rrl_file:
            rule2weights = rrl.rule_print(db_enc.X_fname, db_enc.y_fname, train_loader, file=rrl_file, mean=db_enc.mean, std=db_enc.std)
    else:
        rule2weights = rrl.rule_print(db_enc.X_fname, db_enc.y_fname, train_loader, mean=db_enc.mean, std=db_enc.std, display=False)
    
    metric = 'Log(#Edges)'
    edge_cnt = 0
    connected_rid = defaultdict(lambda: set())
    ln = len(rrl.net.layer_list) - 1
    for rid, w in rule2weights:
        connected_rid[ln - abs(rid[0])].add(rid[1])
    while ln > 1:
        ln -= 1
        layer = rrl.net.layer_list[ln]
        for r in connected_rid[ln]:
            con_len = len(layer.rule_list[0])
            if r >= con_len:
                opt_id = 1
                r -= con_len
            else:
                opt_id = 0
            rule = layer.rule_list[opt_id][r]
            edge_cnt += len(rule)
            for rid in rule:
                connected_rid[ln - abs(rid[0])].add(rid[1])
    logging.info('\n\t{} of RRL  Model: {}'.format(metric, np.log(edge_cnt)))



def train_main(args):
    os.environ['MASTER_ADDR'] = args.master_address
    os.environ['MASTER_PORT'] = args.master_port
    # mp.spawn(train_model, nprocs=args.gpus, args=(args,))
    train_model(0, args)


if __name__ == '__main__':
    from args import rrl_args
    for arg in vars(rrl_args):
        print(arg, getattr(rrl_args, arg))
    train_main(rrl_args)
    test_model(rrl_args)
