import jieba
import OpenHowNet

# OpenHowNet.download()
hownet_dict = OpenHowNet.HowNetDict()
hownet_dict_advanced = OpenHowNet.HowNetDict(init_sim=True)
file = open("D:\\1353776970\\文件接收＋\\外卖评论.csv", "r", encoding="utf-8")
line = file.readline()
positive_list = ["美味", "迅速", "支持", "多", "开心"]
negative_list = ["恶心", "稀少", "虫子", "slow", "昂贵"]  # "太慢", "太少"
p_result_list = dict()
n_result_list = dict()


def deal_with_str(str_list):
    while '，' in str_list:
        str_list.remove('，')
    while '\n' in str_list:
        str_list.remove('\n')
    while '。' in str_list:
        str_list.remove('。')
    while '！' in str_list:
        str_list.remove('！')


def p_oneword(oneword, list_p, list_n):
    if oneword not in p_result_list:
        Polarity = 0
        Polarity1 = 0
        Polarity2 = 0
        for test_word in list_p:
            Polarity1 += hownet_dict_advanced.calculate_word_similarity(oneword, test_word)
        Polarity1 = Polarity1 / len(list_p)
        for test_word in list_n:
            Polarity2 += hownet_dict_advanced.calculate_word_similarity(oneword, test_word)
        Polarity2 = Polarity2 / len(list_n)
        Polarity = Polarity1 - Polarity2
        p_result_list[oneword] = Polarity
    else:
        pass


def p_word_deal(str_list):
    while str_list:
        p_oneword(str_list.pop(0), positive_list, negative_list)
    return


def n_oneword(oneword, list_p, list_n):
    if oneword not in n_result_list:
        Polarity = 0
        Polarity1 = 0
        Polarity2 = 0
        for test_word in list_p:
            Polarity1 += hownet_dict_advanced.calculate_word_similarity(oneword, test_word)
        Polarity1 = Polarity1 / len(list_p)
        for test_word in list_n:
            Polarity2 += hownet_dict_advanced.calculate_word_similarity(oneword, test_word)
        Polarity2 = Polarity2 / len(list_n)
        Polarity = Polarity1 - Polarity2
        n_result_list[oneword] = Polarity
    else:
        pass


def n_word_deal(str_list):
    while str_list:
        n_oneword(str_list.pop(0), positive_list, negative_list)
    return


def dealwithdict(list, dict):
    for i in list:
        if i in dict:
            del dict[i]


while True:
    line = file.readline()
    if line:
        case = int(line[0])
        # seg_list = jieba.cut(line[2:], cut_all=True)
        seg_list = jieba.cut_for_search(line[2:])
        seglist = list(seg_list)

        deal_with_str(seglist)
        if case == 1:
            p_word_deal(seglist)
        else:
            n_word_deal(seglist)
    else:
        break
p_result_list_ordered = sorted(p_result_list.items(), key=lambda x: x[1], reverse=True)
n_result_list_ordered = sorted(n_result_list.items(), key=lambda x: x[1], reverse=False)
positive_file = open("positive_word.txt", "w")
negative_file = open("negative_word.txt", "w")

rp_dict = dict(p_result_list_ordered[0:60])
np_dict = dict(n_result_list_ordered[0:60])
dealwithdict(positive_list, rp_dict)
dealwithdict(negative_list, np_dict)
i = 1
for key, value in rp_dict.items():
    if i > 50:
        break
    positive_file.write(str(i)+":" +key + "\n")
    i += 1
i = 1
for key, value in np_dict.items():
    if i > 50:
        break
    negative_file.write(str(i)+":" +key + "\n")
    i += 1
file.close()
positive_file.close()
negative_file.close()
