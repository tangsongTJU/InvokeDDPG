import subprocess
class Node:
    def __init__(self,type_,L,R,id,le):
        self.type_ = type_
        self.L = L
        self.R = R
        self.id = id
        self.le = le

class Tree_node:
    def __init__(self,type_,L,R,id,le):
        self.node_list = []
        self.type_ = type_
        self.L = L
        self.R = R
        self.id = id
        self.le = le


import os
# content = ""
# def list_cmp(node_a,node_b):
#     if node_a.le != node_b.le:
#         return node_a.le - node_b.le
#     else:
#         return node_b.id - node_a.id

# def node_list_cmp(x,y):
#     return x-y

# def run(obj):
#     print(obj.id)
#     # obj.node_list.sort()
#     for element in obj.node_list:
#         run(Tree_list[element])



# dirPath = "D:\\datasetforTBCCD-master\\Graduate_experiment-master\\opo_js\\test_target_file2\\"
# m = 0
# files = os.listdir(dirPath)
def _pad_nobatch(children):
    child_len = max([len(c) for n in children for c in n])
    children = [[c + [0] * (child_len - len(c)) for c in sample] for sample in children]
    return children

function = 0

# def dfs_norm(Tree_node,Tree):
#     global function
#     if function == 1 and Tree_node.type!='(':
#         Tree_node.type_ = 'function_name'
#         function = 0
#     elif function == 1 and Tree_node.type =='(':
#         function = 0
#     elif function == 0 and Tree_node.type_ == 'function':
#         function = 1
#
#     for ele in Tree_node.node_list:
#         dfs_norm(Tree[ele],Tree)


def getData_finetune(l,dictt,embeddings):
    nodes11 = []
    children11 = []
    nodes22 = []
    children22 = []
    label = l[1]
    sample = dictt[l[0]]
    queue1 = [(sample[0], -1)]
    while queue1:
        node1, parent_ind1 = queue1.pop(0)
        node_ind1 = len(nodes11)
        queue1.extend([(sample[child], node_ind1) for child in node1.node_list])
        children11.append([])
        if parent_ind1 > -1:
            children11[parent_ind1].append(node_ind1)
        nodes11.append(embeddings[node1.type_])

    children111 = []
    batch_labels = []
    children111.append(children11)
    children1 = _pad_nobatch(children111)
    batch_labels.append(label)
    return nodes11, children1, batch_labels



def getData_finetune_withoutlabel(l,dictt,embeddings):
    nodes11 = []
    children11 = []
    nodes22 = []
    children22 = []
    # label = l[1]
    sample = dictt[l]
    queue1 = [(sample[0], -1)]
    while queue1:
        node1, parent_ind1 = queue1.pop(0)
        node_ind1 = len(nodes11)
        queue1.extend([(sample[child], node_ind1) for child in node1.node_list])
        children11.append([])
        if parent_ind1 > -1:
            children11[parent_ind1].append(node_ind1)
        nodes11.append(embeddings[node1.type_])

    children111 = []
    # batch_labels = []
    children111.append(children11)
    children1 = _pad_nobatch(children111)
    # batch_labels.append(label)
    return nodes11, children1


def get_tree(file_name):
    print(file_name)
    p = subprocess.Popen("java -jar /home/tangsong/Projects/tbcnn-terminal/AT1.jar "+file_name,shell=True,stdout=subprocess.PIPE)
    text = str(p.stdout.read(),encoding = "utf-8")
    p.wait()
    # execute_file_name = "D:/datasetforTBCCD-master/Graduate_experiment-master/opo_js/test_target_file2/"+file_name+".txt"
    text = text.rstrip('\r')
    # file=open(execute_file_name)
    # print(file_name)
    # text=file.read()
    list_x = text.split('\n')

    Tree_list = []
    list = []
    i = 0
    length = len(list_x)
    while len(list_x[i]) > 1:
        temp_ = list_x[i].split(' ,,, ')
        print(temp_)
        type_ = temp_[0]
        L = int(temp_[1])
        R = int(temp_[2])
        id = int(temp_[3])
        le = int(temp_[4])
        if type_.startswith('"') or type_.startswith("'") or type_.startswith('/*'):
            i += 1
            continue
        node = Node(type_,L,R,id,le)
        list.append(node)
        node2 = Tree_node(type_,L,R,id,le)
        Tree_list.append(node2)
        i += 1
    list = sorted(list,key=lambda x:(x.le, -x.id))
    for i in range(len(list)):
        if list[i].le == -1:
            continue;
        for j in range(i+1,len(list)):
            if list[i].le <= list[j].le and list[i].L >= list[j].L and list[i].R <= list[j].R:
                Tree_list[list[j].id].node_list.append(list[i].id)
                # print(list[i].id,list[j].id)
                break
    for ele in Tree_list:
        ele.node_list.sort()
    # dfs_norm(Tree_list[0],Tree_list)
    print(Tree_list)
    return Tree_list,len(Tree_list)
    # run(Tree_list[0])

# get_tree('/home/tangsong/CLionProjects/InvokeDDPGtest/test.js')
# print(Tree_list)
# f = open('/home/doubi/opo_js/target_2/vector_2', 'w')
# f.write(content)
# f.close()
