import os
import tensorflow as tf
import numpy as np
import network3
from sampleJS import get_tree
from sampleJS import getData_finetune
from parameters import EPOCHS, LEARN_RATE
from sklearn.metrics import precision_score, recall_score, f1_score

def train_model(infile, embeddings):
    global threaholder
    threaholder = 0
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    num_feats = 100
    nodes_node1, children_node1, res = network3.init_net_finetune(num_feats,embeddingg)
    aaa = 1
    aaaa = 1
    # out_v = network3.out_layer(res)
    b = tf.constant(value=1, dtype=tf.float32)
    logits_evel = tf.multiply(res, b, name='logits_eval')
    labels_node, loss_node, acc = network3.loss_layer(logits_evel)
    optimizer = tf.train.GradientDescentOptimizer(LEARN_RATE)
    train_step = optimizer.minimize(loss_node)
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)  # config=tf.ConfigProto(device_count={'GPU':0}))

    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())

    # labels_node, accuracy = network3.acc(res)


    dictt = {}
    listrec = []
    f = open("D:\\datasetforTBCCD-master\\test_getSentenceJS\\flist_JSC.txt", 'r')
    line = f.readline().rstrip('\t')
    l = line.split('\t')
    z = 0
    for ll in l:
        if not os.path.exists(ll):
            listrec.append(ll)
            continue
        faa = open(ll, 'r', encoding="utf-8")
        fff = faa.read()
        content = ll.split('/')
        sample, size = get_tree(content[len(content)-1])
        if size > 3000 or size < 10:
            z += 1
            listrec.append(ll)
            continue
        dictt[ll] = sample
        # print(sample)
    f.close()
    print("wuxiaogeshu:", z)
    max_ACC = 0.0
    ssss_loss = []
    ssss_acc = []
    for epoch in range(1, EPOCHS + 1):
        train_loss, train_acc, n_batch = 0, 0, 0
        f = open(infile, 'r')
        line = "123"
        k = 0
        batch_q = []
        while line:
            line = f.readline().rstrip('\n')
            l = line.split('\t')
            # m = l[0] in listrec
            if len(l) != 2:
                break
            if l[0] in listrec:
                continue
            k += 1
            nodes11,children1,batch_labels=getData_finetune(l,dictt,embeddings)
            # print(children1)
            batch_q.append([batch_labels])
            batch_s = int(batch_labels[0])
            # bb_labels = [batch_labels[0] for _ in range(50)]
            _, err, accur, r = sess.run(
                [train_step, loss_node, acc, res],
                feed_dict={
                    nodes_node1: nodes11,
                    children_node1: children1,
                    labels_node: [batch_s],
                }
            )
            train_loss += err
            train_acc += accur
            n_batch += 1
            # if aaa % 500 == 0:
            #     print('Epoch:', epoch,
            #           'Step:', aaa,
            #           'Loss:', train_loss/n_batch,
            #           'ACC:',train_acc/n_batch,
            #           'R:', r,
            #           )
            #     max_ACC = max(train_acc/n_batch,max_ACC)
            #     # saver.save(sess, "./model_o/model.ckpt")

            aaa += 1
        f.close()

        dev_loss, dev_acc, dev_batch = 0, 0, 0
        dev_acc_array = []
        f = open('D:/datasetforTBCCD-master/test_getSentenceJS/JSC_test/devdata.txt', 'r')
        line = "123"
        k = 0
        dev_batch_q = []
        while line:
            line = f.readline().rstrip('\n')
            l = line.split('\t')
            # m = l[0] in listrec
            if len(l) != 2:
                break
            if l[0] in listrec:
                continue
            k += 1
            nodes11, children1, batch_labels = getData_finetune(l, dictt, embeddings)
            # print(children1)
            dev_batch_q.append([batch_labels])
            dev_batch_s = int(batch_labels[0])
            # bb_labels = [batch_labels[0] for _ in range(50)]
            err, accur, r = sess.run(
                [loss_node, acc, res],
                feed_dict={
                    nodes_node1: nodes11,
                    children_node1: children1,
                    labels_node: [dev_batch_s],
                }
            )
            dev_loss += err
            dev_acc += accur
            dev_batch += 1
            if aaaa % 80 == 0:
                print('Epoch:', epoch,
                      'Step:', aaaa,
                      'Loss:', dev_loss / dev_batch,
                      'ACC:', dev_acc / dev_batch,
                      'R:', r,
                      )
                ssss_acc.append(dev_acc / dev_batch)
                ssss_loss.append(dev_loss / dev_batch)
                # max_ACC = max(train_acc / n_batch, max_ACC)
                # saver.save(sess, "./model_o/model.ckpt")
                file3 = open('22ew.txt', 'a')
                file4 = open('3.txt', 'a')
                file3.write(str(dev_acc / dev_batch)+";")

                file4.write(str(dev_loss / dev_batch)+";")
                file3.close()
                file4.close()

            aaaa += 1

        f.close()




        # correct_labels_dev = []
        # predictions_dev = []
        # for i in range(0, 15):
        #     predictions_dev.append([])
        # ff = open("./datasetForVariantsTBCCD/BCB/devdata.txt", 'r')
        # line = "123"
        # k = 0
        # maxf1value = -1.0
        # while line:
        #     line = ff.readline().rstrip('\n')
        #     l = line.split('\t')
        #     if len(l) != 3:
        #         break
        #     if (l[0] in listrec) or (l[1] in listrec):
        #         continue
        #     label = l[2]
        #     k += 1
        #     nodes11, children1, nodes22, children2, _ = getData_finetune(l, dictt, embeddings)
        #     output = sess.run([res],
        #                       feed_dict={
        #                           nodes_node1: nodes11,
        #                           children_node1: children1,
        #
        #                       }
        #                       )
        #     correct_labels_dev.append(int(label))
        #     threaholder = -0.7
        #     for i in range(0, 15):
        #         if output[0] >= threaholder:
        #             predictions_dev[i].append(1)
        #         else:
        #             predictions_dev[i].append(-1)
        #         threaholder += 0.1
        # for i in range(0, 15):
        #     f1score = f1_score(correct_labels_dev, predictions_dev[i], average='binary')
        #     if f1score > maxf1value:
        #         maxf1value = f1score
        #         maxstep = i
        #
        # ff.close()
        # correct_labels_test = []
        # predictions_test = []
        # ff = open("./datasetForVariantsTBCCD/BCB/testdata.txt", 'r')
        # line = "123"
        # k = 0
        # while line:
        #     line = ff.readline().rstrip('\n')
        #     l = line.split('\t')
        #     if len(l) != 3:
        #         break
        #     k += 1
        #     label = l[2]
        #
        #     if (l[0] in listrec) or (l[1] in listrec):
        #         continue
        #     nodes11, children1, nodes22, children2, _ = getData_finetune(l, dictt, embeddings)
        #     output = sess.run([res],
        #                       feed_dict={
        #                           nodes_node1: nodes11,
        #                           children_node1: children1,
        #                       }
        #                       )
        #     correct_labels_test.append(int(label))
        #     threaholder = -0.7+maxstep*0.1
        #     if output[0] >= threaholder:
        #         predictions_test.append(1)
        #     else:
        #         predictions_test.append(-1)
        # print("starttest:\n")
        # print("threaholder:")
        # print(threaholder)
        # p = precision_score(correct_labels_test, predictions_test, average='binary')
        # r = recall_score(correct_labels_test, predictions_test, average='binary')
        # f1score = f1_score(correct_labels_test, predictions_test, average='binary')
        # print("recall_test:" + str(r))
        # print("precision_test:" + str(p))
        # print("f1score_test:" + str(f1score))
        # ff.close()


if __name__ == '__main__':
    dictt = {}
    dictta = {}
    listta = list()
    def _onehot(i, total):
        return [1.0 if j == i else 0.0 for j in range(total)]
    feature_size = 100
    fz = open("new 1.txt", 'r')
    line = "123"
    listchar = []
    while line:
        line = fz.readline().rstrip("\n")
        l = line.split(" ")
        listchar.extend(list(set(l)))
        listchar = list(set(listchar))
        # print(1)
    fz.close()
    for l in listchar:
        listta.append(np.random.normal(0, 0.1, 100).astype(np.float32))
    embeddingg = np.asarray(listta)
    embeddingg = tf.Variable(embeddingg)
    for i in range(len(listchar)):
        dictta[listchar[i]] = i
    train_model('D:/datasetforTBCCD-master/test_getSentenceJS/JSC_test/traindata.txt', dictta)