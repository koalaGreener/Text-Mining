from math import log

# this function will be used when calculate the nqi_list(the number of documents containing qi)
def func(qi, document_num_name):
    nqi = 0
    for item in document_num_name:
        if ((qi) in document_num_name[item]):
            nqi += 1
    return nqi


# Implemented the BM25 algorithm
def BM25(document_name, query_name):
    # the list of 'return_value' is contained with the answer
    return_value = []

    # Parameters
    b = 0.75
    k = 1.5
    avgdl = 0.0  # 1374.882219471947
    N = 4848    # The length of the document, so that we can calcuate the "AVGDL"

    # store the data in those lists
    query_id = dict()
    document_id = []
    document_only_num_list = []
    document_length = dict()
    document_num_name = dict()

    # read the query
    # query_id  return  {201: [1139, 3209], 202: [33, 33410, 19539], 203: [1449, 505, 4155].....}
    # the value in query are 1, so we don't need to put them into the dict
    with open(query_name) as infile:
        for line in infile:
            temp = []
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                temp.append(int(line[i].split(":")[0]))
            query_id[int(line[0])] = temp

    # read the document
    # fulfill the  "document_length" and "document_num_name" dicts
    # document_length  return {'clueweb12-1500wb-53-18853': 688, 'clueweb12-0005wb-40-20687': 379....}
    # document_num_name return { 'clueweb12-1500wb-53-18853' : {5046: 1, 1016: 1, 1018: 1, 122879 : 1....}}
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

    # "avgdl" calculated
    sum = 0
    for every in document_only_num_list:
        sum += int(every.split(":")[1])
    avgdl = 1.0 * sum / N

    # nqi list(the number of documents containing qi)
    # nqi_list return {8192: 220, 769: 1179, 29958: 146, 7: 1553, 3848: 208, 2059: 140....}
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
        # The second iteration
        for document_item in document_id:
            score = 0.0

            # "D" = the length of the document D in words
            D = document_length.get(document_item.split(" ")[0])

            # calculated each query_term's score and then added them into score
            for qi in qi_list:

                # "fqid" calculated
                fqid = 0
                fqid_dict = document_num_name.get(document_item)
                # if the term doesn't exist, then return 0
                if fqid_dict.get(qi) is None:
                    fqid = 0
                else:
                    fqid = fqid_dict.get(qi)

                # "nqi" calculated
                nqi = nqi_list.get(qi)

                # score calculated, the same as the given one, but all of the parameter have been already calcualted
                score += (log((N - nqi + 0.5) / (nqi + 0.5))) * 1.0 * fqid * (k + 1) / (fqid + k * (1 - b + (b * D / avgdl)))

                # put the score in sorted_map via the document_key
                sorted_map[document_item] = score

        # Before the output, we need to use the sort function to sort it by value
        ranked_result = sorted(sorted_map.items(), key=lambda x: x[1])
        ranked_result.reverse()

        # output the formatted result
        for everyitem in ranked_result:
            # output all of the formateed data
            # print(str(query_item) + " Q0 " + str(everyitem).strip("' ( '").split("',")[0] + " " + str(ranking) + str(everyitem).strip("'( ')").split(",")[1] + " bm25")
            return_value.append(
                str(query_item) + " Q0 " + str(everyitem).strip("' ( '").split("',")[0] + " " + str(ranking) +
                str(everyitem).strip("'( ')").split(",")[1] + " bm25")
            ranking += 1
    return return_value


######################################## # main function Started here ################################################
if __name__ == '__main__':
    '''import the data's file path'''
    return_value = BM25("../data/Q1/document_term_vectors.dat", "../data/Q1/query_term_vectors.dat")
    # return_value -> ['246 Q0 clueweb12-1002wb-20-18538 4038 0.0 bm25', '246 Q0 clueweb12-0502wb-96-04705 4039 0.0 bm25'.....]
    print(return_value)