import sampleJS
import os

numnodes = 0
def dfsDict(root,sample):
    global listtfinal
    listtfinal.append(str(root.type_))
    global numnodes
    numnodes += 1
    if len(root.node_list):
        pass
    else:
        return
    for dictt in root.node_list:
        dfsDict(sample[dictt],sample)

f=open("sentence_JSC.txt",'w')
listfile=os.listdir("D:/datasetforTBCCD-master/jsc-CVE")
#print(listfile)
lisfinalfile=[]
ff=open("D:/datasetforTBCCD-master/test_getSentenceJS/flist_JSC.txt",'w')
i = 0
for lis in listfile:
    ff.write("D:/datasetforTBCCD-master/jsc-CVE/"+lis+'\t')
    lisfinalfile.append("D:/datasetforTBCCD-master/jsc-CVE/"+lis)
    i += 1
#print(lisfinalfile)
ff.close()
# f = open("D:/datasetforTBCCD-master/test_getSentenceJS/flist_JSC.txt", 'r')
# line = f.readline().rstrip('\t')
# l = line.split('\t')
print("xxxxxx")

for l in lisfinalfile:
    if not os.path.exists(l):
        continue
    # ff=open(l,'r')
    # z+=1
    # content=ff.read()
    # print(l)
    # tree = javalang.parse.parse_member_signature(content)
    file_names = l.split('/')
    file_name = file_names[len(file_names)-1]
    sample, size = sampleJS.get_tree(file_name)
    listtfinal = []
    dfsDict(sample[0],sample)
    for lisf in listtfinal:
        print(lisf)
        f.write(lisf)
        f.write(" ")
    f.write("\n")
f.close()



# file_path = "D:\\datasetforTBCCD-master\\Graduate_experiment-master\\opo_js\\test_target_file2\\"
# file_name = "16bit-code.js.txt"
# sample,size = sampleJS.get_tree(file_path + file_name)
# print(sample)
# listtfinal = []
# dfsDict(sample[0],sample)
# for lisf in listtfinal:
#     print(lisf)
