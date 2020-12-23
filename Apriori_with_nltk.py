#Algorithm code from https://github.com/KezhiAdore/BilibiliAnimeData_Analysis

def readtitle():
    l = []
    for i in open("dataL.csv"):
        q = int(i.find("|"))
        l.append(i[0:q])
        # print(i[0:q]+'\n'+i[q+1:-1])
    # print(l)
    # print(l)
    q = []
    for i in l:
        q.append(i.split(' '))
    #print(q)
    return q


def readabstract():
    l = []
    for i in open("dataL.csv"):
        q = int(i.find("|"))
        l.append(i[q+1:-2])
        # print(i[0:q]+'\n'+i[q+1:-1])
    # print(l)
    # print(l)
    q = []
    for i in l:
        q.append(i.split(' '))
    #print(q)
    return q
#print(readabstract())



l1=[]



from nltk.corpus import stopwords # 需要下载stopwords

#针对标题
#words=readtitle()

#针对摘要（需要分别处理）
words=readtitle()

for iwords in words:
    filtered_words = [word for word in iwords if word not in stopwords.words('english')]
  #  print('原始词：', iwords)
  #  print('去除停用词后：', filtered_words)
    l1.append(filtered_words)

tags=l1

#print(l1)


# Apriori算法连接步 单步实现


def merge_list(l1, l2):
    length = len(l1)
    for i in range(length-1):
        if l1[i] != l2[i]:
            return 'nope'
    if l1[-1] != l2[-1]:
        l = l1.copy()
        l.append(l2[-1])
        return l
    else:
        return 'nope'

# 判断l2是否包含在l1中


def is_exist(l1, l2):
    for i in l2:
        if i not in l1:
            return False
    return True

# 利用min_sup和min_conf进行剪枝,即最小支持度和最小置信度,L_last为k-1项频繁集


def prune(L=[], L_last=0, min_sup=0, min_conf=0):
    tmp_L = []
    if L_last == 0 or min_conf == 0:
        for index, l in enumerate(L):
            if l[1] < min_sup:
                continue
            tmp_L.append(l)
    else:
        for index, l in enumerate(L):
            if l[1] < min_sup:
                continue
            for ll in L_last:
                if l[0][:-1] == ll[0]:
                    if l[1]/ll[1] >= min_conf:
                        tmp_L.append(l)
    return tmp_L


def Apriori(data, min_sup, min_conf):
    # C:临时存储k项集  L:临时存储频繁k项集  L_save:保存频繁1-k项集
    C, L, L_save = [], [], []
    # 使用支持度计数来代替支持度进行计算
    min_sup_count = min_sup*len(data)
    # 初始化一项集
    for tags in data:
        for tag in tags:
            if C == [] or [tag] not in [x[0] for x in C]:
                C.append([[tag], 0])
    # 筛选出频繁一项集
    L = C.copy()
    for index, l in enumerate(L):
        for tags in data:
            if is_exist(tags, l[0]):
                L[index][1] += 1
    L = prune(L, min_sup=min_sup_count)
    L_save.append(L)
    while True:
        # 由频繁k-1项集构造k项集
        C = []
        for l1 in L:
            for l2 in L:
                list_merge = merge_list(l1[0], l2[0])
                if list_merge != 'nope':
                    C.append([list_merge, 0])
        # 统计频次，剪枝
        L = C.copy()
        for index, l in enumerate(L):
            for tags in data:
                if is_exist(tags, l[0]):
                    L[index][1] += 1
        L = prune(L, L_save[-1], min_sup_count, min_conf)
        # L=空集时结束循环
        if L == []:
            return L_save
        L_save.append(L)



ans = Apriori(tags, 0.02, 0.5)
# 只输出最多的频繁项
print(ans)
for i in ans[-1]:
    print(i)