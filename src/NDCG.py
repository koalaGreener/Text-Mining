from math import log2


def readTheFile_idcg(filename):
    term_rankging_score = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            temp = {}
            each = line.split(" ")
            id = each[0]
            ranking = each[3]
            score = each[4]
            if int(ranking) < 50:
                term_rankging_score.append(str(id) + " " + str(ranking) + " " + str(score))
        return term_rankging_score


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


if __name__ == '__main__':

    idcg_term_rankging_score = readTheFile_idcg("../data/BM25b0.75_0.res")
    idcg_value = calculated_DCG_score(idcg_term_rankging_score)
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
