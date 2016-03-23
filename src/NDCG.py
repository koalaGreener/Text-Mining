from math import log2


def readTheFile_dcg(filename):
    term_rankging_score = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            if int(line.split(" ")[3]) < 50:
                term_rankging_score.append(line.split(" ")[0] + " " + line.split(" ")[2])
        return term_rankging_score


def readTheFile_rel(filename):
    with open(filename) as infile:
        full_dict = {}
        for line in infile:
            # str:int
            temp_dict = {}
            full_dict[line.split(" ")[0] + " " + line.split(" ")[2]] = int(line.split(" ")[3])
        return full_dict
        # print(full_dict)

def readTheFile_term(filename):
    with open(filename) as infile:
        return_value = {}
        for line in infile:
            return_value[(line.split(" ")[0])] = ""
    return return_value


def calculated_DCG_score(input_data):
    preprocessed_output_dict = {}
    ranking_score = {}
    return_dcg_term_value = {}
    count = 0
    for data in input_data:
        id = data.split(" ")[0]
        ranking = data.split(" ")[1]
        score = data.split(" ")[2]
        # print(id,ranking,score)
        ranking_score[ranking] = score
        count += 1
        if count == 50:
            preprocessed_output_dict[id] = ranking_score
            ranking_score = {}
            count = 0
    count = 0
    for data in preprocessed_output_dict:
        # data = 201
        # K:score
        dcg_value = {}
        ranking_score_dict = preprocessed_output_dict.get(data)
        for i in range(1, 51):
            temp_dcg_sum = 0.0
            if i == 1:
                dcg = ranking_score_dict.get(str(i - 1))
                temp_dcg_sum += float(dcg)
                dcg_value[i] = float(dcg)
            else:
                dcg = temp_dcg_sum + float(ranking_score_dict.get(str(i - 1))) / log2(i)
                dcg_value[i] = float(dcg)
        count += 1
        # print(data, dcg_value)
        return_dcg_term_value[data] = dcg_value
    # print(count)
    return return_dcg_term_value


def calculate_ndcg(term_id, k, term_docid, term_docid_rel_dict):
    rel_list = []
    start_index = 50 * (int(term_id) - 201)
    end_index = start_index + k
    #print(start_index, end_index)
    for i in range (start_index, end_index):
        #print(term_docid[i])
        #print(term_docid_rel_dict.get(term_docid[i]))
        rel_list.append(term_docid_rel_dict.get(term_docid[i]))
    #print(rel_list)
    return rel_list


if __name__ == '__main__':

    # output the data with (id + ranking + score)
    term_docid = readTheFile_dcg("../data/BM25b0.75_0.res")
    print(term_docid)
    #print(len(term_docid))

    # intput the data of Rel (str:int)
    term_docid_rel_dict = readTheFile_rel("../data/qrels.adhoc.txt")
    print(term_docid_rel_dict)

    #only the term id int
    term_dict = readTheFile_term("../data/BM25b0.75_0.res")
    print(term_dict)

    #Every Term
    for term_id in term_dict:
        #print("Term:   " + str(term_id))

        #这里term_id 不是彻底的1-250 所以函数里面的 term_id-201会越界 因为会最后超出 只有2400个
        for k in (1, 2):
            rel_list = calculate_ndcg(249, k, term_docid, term_docid_rel_dict)





'''
    # calculated the NDCG score
    k_score = {}
    term_k_score = {}
    # print((dcg_value))
    # print((idcg_value))

    # calculate the NDCG
    for index_term in idcg_value:
        k_score = {}
        for index_K in range(1, 51):
            ndcg = idcg_value[index_term][index_K]
            k_score[index_K] = ndcg
        term_k_score[index_term] = k_score

    print(term_k_score)
'''
