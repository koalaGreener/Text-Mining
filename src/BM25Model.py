from math import log

def func(qi, document_num_name):
    nqi = 0
    for item in document_num_name:
        if((qi) in document_num_name[item]):
            nqi += 1
    return nqi

def readTheFile(document_name, query_name):
    b = 0.75
    k = 1.5
    avgdl = 0.0  # 1374.882219471947
    N = 4848
    # store the data in this two list
    query_id = {}
    document_id = []
    with open(document_name) as infile:
        for line in infile:
            document_id.append(line.split(" ")[0])

    with open(query_name) as infile:
        for line in infile:
            temp = []
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                temp.append(int(line[i].split(":")[0]))
            query_id[int(line[0])] = temp


    document_only_num_list = []
    document_length = {}
    document_num_name = {}
    with open(document_name) as infile:
        for line in infile:
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

    #print(document_num_name)
    # avgdl calculated
    sum = 0
    for every in document_only_num_list:
        sum += int(every.split(":")[1])
    avgdl = 1.0 * sum / N
    #print(avgdl)



    print("start nqi")

    #nqi list
    nqi_list = {}
    for query_item in query_id:
        qi_list = query_id.get(query_item)
        for qi_value in qi_list:
            nqi_list[qi_value] = func(qi_value, document_num_name)

    print("end nqi")
    for query_item in query_id:
        # index 保存query中所出现的 term
        qi_list = query_id.get(query_item)
        #print(qi_list)
        count = 0
        for document_item in document_id:
            score = 0.0

            # D = the length of the document D in words
            D = document_length.get(document_item.split(" ")[0])

            for qi in qi_list:

                #fqid 计算
                fqid = 0
                fqid_dict = document_num_name.get(document_item)
                if fqid_dict.get(qi) == None:
                    fqid = 0
                else:
                    fqid = fqid_dict.get(qi)

                #nqi 计算
                nqi = nqi_list.get(qi)

                #score 计算
                score += (log((N - nqi + 0.5) / (nqi + 0.5))) * 1.0 * fqid * (k + 1)/ (fqid + k * (1 - b + (b * D / avgdl)))
                print(count, query_item, document_item, score)
            count += 1


'''import the data'''
if __name__ == '__main__':
    readTheFile("../data/document_term_vectors.dat", "../data/query_term_vectors.dat")
