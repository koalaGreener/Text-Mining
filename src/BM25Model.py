def readTheFile(document_name, query_name):
    b = 0.75
    k = 1.5
    avgdl = 0.0 #1374.882219471947
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



    #avgdl calculated
    sum = 0
    document_num = 4848
    for every in document:
        split_after = every.split(" ")
        for any_data in split_after:
            if (any_data[0] != "c" and len(any_data) != 1):
                value = any_data.split(":")
                sum += int(value[1])
    avgdl = 1.0 * sum / document_num
    #print(sum)


    for query_item in query:
        for document_item in document:
            



'''import the data'''
if __name__ == '__main__':
    readTheFile("../data/document_term_vectors.dat", "../data/query_term_vectors.dat")



'''
    for query_item in query:
        for document_item in document:
'''