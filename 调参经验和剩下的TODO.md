我大概读了下 RRL，知道了每个网络层是怎么设计的（binary层->逻辑运算层->nn.Linear。对于输入的离散值，做onehot encoding后送入binary层，对于连续值，量化到 n 个 level 后送入 binary 层；其中逻辑运算层模拟交和并，训练时用连续的函数反向传播，其函数特性决定了推理时每条weight容易被量化成 0/1 值；Linear 就是普通的 Linear 层，用于连接逻辑运算层和输出层）。但是对于逻辑运算层的实现我没认真看，如果要做bonus的话这里可以试着做些优化。

还有 baseline 没做，调参没仔细搜索，展示材料分工没分。运行方式放在 train.sh 里了。任务 1 上最好需要调到和paper里汇报的结果一样，后面两个越高肯定是越好。

任务一 bank-marketing bin-classification / ours F1 72.03 / reported 77.18
任务二 housing regression / ours MSE 35.28
任务三 breast-cancer bin-classification / ours F1 77.38


- 这个 weight decay 加的很sb，他没有对参数的个数取平均，而是直接加在所有参数上（可能这个是任务 1 没复现好的重点）
- 我试着改深模型反而效果在任务3上变差了（其他两个任务看起来没太大变化），have no idea why

