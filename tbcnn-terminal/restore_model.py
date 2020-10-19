import os
import tensorflow as tf
import numpy as np
import network3
from sampleJS import get_tree
from sampleJS import getData_finetune_withoutlabel
from parameters import EPOCHS, LEARN_RATE
# 加载模型
sess = tf.Session()
# get_tree("/home/tangsong/CLionProjects/InvokeDDPGtest/test.js")
current_path = os.getcwd()
saver = tf.train.import_meta_graph("/home/tangsong/CLionProjects/InvokeDDPGtest/tbcnn-terminal/model_o/model.ckpt.meta")
saver.restore(sess, tf.train.latest_checkpoint("/home/tangsong/CLionProjects/InvokeDDPGtest/tbcnn-terminal/model_o"))
# #
# 需要用到的参数，需要从池化层得到向量
graph = tf.get_default_graph()
nodes_node1 = graph.get_tensor_by_name("inputs/tree:0")
children_node1 = graph.get_tensor_by_name("inputs/children:0")
pool_out = graph.get_tensor_by_name("network/pooling/Max:0")
#
# 获得embedding索引表
embeddings_index = {}
fz = open("/home/tangsong/CLionProjects/InvokeDDPGtest/tbcnn-terminal/new 1.txt", 'r')
line = "123"
listchar = []
while line:
    line = fz.readline().rstrip("\n")
    l = line.split(" ")
    listchar.extend(list(set(l)))
    listchar = list(set(listchar))
    # print(1)
fz.close()
for i in range(len(listchar)):
    embeddings_index[listchar[i]] = i

def fileString_convert_vector(file_path_name):
    # 将文件转为node和children两部分
    #########正文开始############
    dictt = {}
    # file_path_name = "D:\\tbcnn_\\CVE-2018-4441.js"
    sample, size = get_tree(file_path_name)
    dictt[file_path_name] = sample
    nodes11,children1 = getData_finetune_withoutlabel(file_path_name,dictt,embeddings_index)
    out_put = sess.run(
                    [pool_out],
                    feed_dict={
                        nodes_node1: nodes11,
                        children_node1: children1,
                    }
                )
    return out_put


# # def test():
# print(len(fileString_convert_vector('/home/tangsong/CLionProjects/InvokeDDPGtest/test.js')[0][0]))

