# Write a python script to preprocess a dbc file like this
# // Data Base. Elvira Format

# data-base breastCancer_Test {
# number-of-cases = 19;


# // Network Variables 

# node SampleType(finite-states) {
# kind-of-node = chance;
# type-of-variable = finite-states;
# relevance = 7.0;
# purpose = "";
# num-states = 2;
# states = (relapse non-relapse);
# }

# node Contig45645_RC (continuous) {
# kind-of-node = chance;
# type-of-variable = continuous;
# relevance = 7.0;
# purpose = "";
# min = -2.0;
# max = 1.058;
# precision = 2;
# }

import numpy as np

# Python
# file = "breastCancer_Test.dbc"
# with open(file, 'r') as f:
#     lines = f.readlines()
#     # find the line number where 'cases' in line. then only consider lines after it.
#     j = 0
#     for i, line in enumerate(lines):
#         j = i
#         if 'cases = (' in line:
#             break
#     # remove the first i lines
#     lines = lines[i:]
    
#     # only keep those lines char len > 20
#     lines = [line for line in lines if len(line) > 20]
    
#     # for each line, replace `[ ` and `]\n` to ''
#     lines = [line.replace('[ ', '').replace(']\n', '') for line in lines]
    
#     data_list = []
    
#     # process each line!
#     for line in lines:
#         new_data = []
#         # split by comma
#         split_line = line.split(', ')
#         # contains float or ?. if float, direct insert. else, insert 'nan'
#         for item in split_line:
#             if item.strip() == 'relapse' or item.strip() == 'non-relapse':
#                 new_data.append(1 if item.strip() == 'relapse' else 0)
#                 continue
            
#             try:
#                 new_data.append(float(item))
#             except:
#                 assert item.strip() == '?', 'item is not ? but {}'.format(item)
#                 new_data.append(np.nan)
#         data_list.append(new_data)
    
#     column_len = len(data_list[0])
#     # assert column length is the same
#     for data in data_list:
#         assert len(data) == column_len
#     print("item len is {}".format(column_len))
        

#     # convert to numpy array
#     # data = np.array(data_list)

#     # save to .data format
#     with open('breast-cancer-test.data', 'w') as f:
#         for i in range(len(data_list)):
#             f.write(','.join([str(x) for x in data_list[i]]) + '\n')
    
    # import IPython; IPython.embed()
    
    # first the cases line
    # if 'cases' in line:
    
with open('breast-cancer.info', 'w') as f:
    
    # Write RESULT discrete
    f.write('RESULT discrete\n')
    
    # Write F{x} continuous, 1 <= x <= 24481
    for i in range(1, 24482):
        f.write('F{} continuous\n'.format(i))
    
    # Write LABEL_POS 0
    f.write('LABEL_POS 0\n')
