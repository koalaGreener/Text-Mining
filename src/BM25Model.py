from math import log, log2


def func(qi, document_num_name):
    nqi = 0
    for item in document_num_name:
        if ((qi) in document_num_name[item]):
            nqi += 1
    return nqi


def readTheFile(document_name, query_name):

    return_value = []
    # Parameters
    b = 0.75
    k = 1.5
    avgdl = 0.0  # 1374.882219471947
    N = 4848

    # store the data in those lists
    query_id = {}
    document_id = []
    document_only_num_list = []
    document_length = {}
    document_num_name = {}

    # read the query
    with open(query_name) as infile:
        for line in infile:
            temp = []
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                temp.append(int(line[i].split(":")[0]))
            query_id[int(line[0])] = temp

    # read the document
    with open(document_name) as infile:
        for line in infile:
            document_id.append(line.split(" ")[0])
            name = ""
            document_only_num_map = {}
            length_of_document = 0
            line = line.rstrip(" \n")
            eachline_list = line.split(" ")
            for eachline in eachline_list:
                if eachline[0] != 'c':
                    document_only_num_list.append(eachline)
                    document_only_num_map[int(eachline.split(":")[0])] = int(eachline.split(":")[1])
                    length_of_document += int(eachline.split(":")[1])
                if eachline[0] == 'c':
                    name = eachline
            document_length[name] = length_of_document
            document_num_name[name] = document_only_num_map

    # avgdl calculated
    sum = 0
    for every in document_only_num_list:
        sum += int(every.split(":")[1])
    avgdl = 1.0 * sum / N

    # nqi list(the number of documents containing qi)
    nqi_list = {}
    for query_item in query_id:
        qi_list = query_id.get(query_item)
        for qi_value in qi_list:
            nqi_list[qi_value] = func(qi_value, document_num_name)

    # Two iterations to calculated the score (first one)
    for query_item in query_id:
        qi_list = query_id.get(query_item)
        sorted_map = {}
        ranking = 0
        #(second one)
        for document_item in document_id:
            score = 0.0

            # D = the length of the document D in words
            D = document_length.get(document_item.split(" ")[0])

            # calculated each query_term's score and then added them into score
            for qi in qi_list:

                # fqid calculated
                fqid = 0
                fqid_dict = document_num_name.get(document_item)
                # if the term doesn't exist, then return 0
                if fqid_dict.get(qi) is None:
                    fqid = 0
                else:
                    fqid = fqid_dict.get(qi)

                # nqi calculated
                nqi = nqi_list.get(qi)

                # score calculated
                score += (log((N - nqi + 0.5) / (nqi + 0.5))) * 1.0 * fqid * (k + 1) / (
                fqid + k * (1 - b + (b * D / avgdl)))
                sorted_map[document_item] = score
        ranked_result = sorted(sorted_map.items(), key=lambda x: x[1])
        ranked_result.reverse()

        # output the formatted result
        for everyitem in ranked_result:
            #print(str(query_item) + " Q0 " + str(everyitem).strip("' ( '").split("',")[0] + " " + str(ranking) + str(everyitem).strip("'( ')").split(",")[1] + " bm25")
            return_value.append(str(query_item) + " Q0 " + str(everyitem).strip("' ( '").split("',")[0] + " " + str(ranking) + str(everyitem).strip("'( ')").split(",")[1] + " bm25")
            ranking += 1
    return return_value

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






'''import the data'''
if __name__ == '__main__':


    def calculated_DCG_score(input_data):
        preprocessed_output_dict = {}
        ranking_score = {}
        return_dcg_term_value = {}
        count = 0
        for data in input_data:
            id = data.split(" ")[0]
            ranking = data.split(" ")[1]
            score = data.split(" ")[2]
            #print(id,ranking,score)
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
                    dcg =  ranking_score_dict.get(str(i - 1))
                    temp_dcg_sum += float(dcg)
                    dcg_value[i] = float(dcg)
                else:
                    dcg = temp_dcg_sum + float(ranking_score_dict.get(str(i - 1))) / log2(i)
                    dcg_value[i] = float(dcg)
            count += 1
            #print(data, dcg_value)
            return_dcg_term_value[data] = dcg_value
        #print(count)
        return return_dcg_term_value


    # import the data
    dcg_data = readTheFile("../data/document_term_vectors.dat", "../data/query_term_vectors.dat")

    dcg_term_rankging_score = []
    value = {}
    for data in dcg_data:
        each = data.split(" ")
        id = each[0]
        ranking = each[3]
        score = each[4]
        if int(ranking) < 50:
            dcg_term_rankging_score.append(str(id) + " " + str(ranking) + " " + str(score))

    idcg_term_rankging_score = readTheFile_idcg("../data/BM25b0.75_0.res")

    # import the data


    dcg_value = calculated_DCG_score(dcg_term_rankging_score)
    idcg_value = calculated_DCG_score(idcg_term_rankging_score)
    k_score = {}
    term_k_score = {}
    #print((dcg_value))
    #print((idcg_value))

    #calculate the NDCG
    for index_term in idcg_value:
        k_score = {}
        for index_K in range(1, 51):
            ndcg = 1.0 * dcg_value[index_term][index_K] / idcg_value[index_term][index_K]
            k_score[index_K] = ndcg
        term_k_score[index_term] = k_score


    print(term_k_score)

'''
    temp1 = 0.0
    temp5 = 0.0
    for i in term_k_score:
        print("----")
        print("topic:" + str(i))
        print("K" + "  " + "NDCG@K")
        print("1" + " " + str(term_k_score[i][1]))
        print("5" + " " + str(term_k_score[i][5]))
        print("10" + " " + str(term_k_score[i][10]))
        print("20" + " " + str(term_k_score[i][20]))
        temp1 += term_k_score[i][1]
        temp5 += term_k_score[i][5]

    print(temp1 / 48)
    print(temp5 / 48)














    def calculated_DCG_score(input_data):
        preprocessed_output_dict = {}
        ranking_score = {}
        return_dcg_term_value = {}
        count = 0
        for data in input_data:
            id = data.split(" ")[0]
            ranking = data.split(" ")[1]
            score = data.split(" ")[2]
            #print(id,ranking,score)
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
                    dcg =  ranking_score_dict.get(str(i - 1))
                    temp_dcg_sum += float(dcg)
                    dcg_value[i] = float(dcg)
                else:
                    dcg = temp_dcg_sum + float(ranking_score_dict.get(str(i - 1))) / log2(i)
                    dcg_value[i] = float(dcg)
            count += 1
            #print(data, dcg_value)
            return_dcg_term_value[data] = dcg_value
        #print(count)
        return return_dcg_term_value



'''