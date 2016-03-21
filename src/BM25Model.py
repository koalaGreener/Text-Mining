from math import log


def readTheFile(document_name, query_name):
    b = 0.75
    k = 1.5
    avgdl = 0.0  # 1374.882219471947
    D = 0
    N = 4848
    # store the data in this two list
    document = [""] * N
    query = [""] * 50
    with open(document_name) as infile:
        index = 0
        for line in infile:
            document[index] = line
            index += 1

    with open(query_name) as infile:
        index = 0
        for line in infile:
            query[index] = line
            index += 1

    # avgdl calculated
    sum = 0
    document_num = 4848
    for every in document:
        split_after = every.split(" ")
        for any_data in split_after:
            if (any_data[0] != "c" and len(any_data) != 1):
                value = any_data.split(":")
                sum += int(value[1])
    avgdl = 1.0 * sum / document_num


    for query_item in query:
        # index 保存query中所出现的 term
        qi_list = []
        query_spited = query_item.split(" ")
        for each_query_item in query_spited:
            if (len(each_query_item) != 3 and len(each_query_item) != 1):
                value1 = each_query_item.split(":")[0]
                qi_list.append(value1)
        for document_item in document:
            # D = the length of the document D in words
            D = 0
            score = 0.0
            document_splited = document_item.split(" ")
            for any in document_splited:
                if (any[0] != "c" and len(any) != 1):
                    item = any.split(":")
                    D += int(item[1])
            for qi in qi_list:
                score += score_function(N, int(qi), document, document_item, k, b, D, avgdl)

            print(score)
def score_function(N, qi, document, document_item, k, b, D, avgdl):
    return IDF(N, qi, document) * qid(document_item, qi) * (k + 1)/ (qid(document_item, qi) + k * (1 - b + (1.0 * b * D / avgdl)))



# IDF function
def IDF(N, qi, document):
    value = log(1.0 * (N - nq(document, qi) + 0.5) / (nq(document, qi) + 0.5))
    return value


# F(Qi,d)
def qid(each_document, qi):
    document_splited = each_document.split(" ")
    for any in document_splited:
        if (any[0] != "c" and len(any) != 1):
            item = any.split(":")
            if (int(item[0]) == qi):
                return int(item[1])

# N(q) calculated
def nq(document, q):
    count = 0
    for document_item in document:
        document_splited = document_item.split(" ")
        for any in document_splited:
            if (any[0] != "c" and len(any) != 1):
                item = any.split(":")
                if (int(item[0]) == q):
                    count += 1
    return count


'''import the data'''
if __name__ == '__main__':
    readTheFile("../data/document_term_vectors.dat", "../data/query_term_vectors.dat")

'''



'''
