#maximal marginal relevance (MMR)
import math

Lambda1 = 0.5
Lambda2 = 0.75


def readTheFile_Query_document_Q1(filename):
    qurey_document = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            qurey_document.append(line.split(" ")[0] + " " + line.split(" ")[2])
        return qurey_document


def readTheFile_query_term_vector(filename):
    query_id = {}
    with open(filename) as infile:
        for line in infile:
            temp = []
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                temp.append(int(line[i].split(":")[0]))
            query_id[int(line[0])] = temp

    return query_id

def readTheFile_document_term_vector(filename):
    document_id = {}
    with open(filename) as infile:
        for line in infile:
            term_id_freqency = {}
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                term_id_freqency[int(line[i].split(":")[0])] = int(line[i].split(":")[1])
                document_id[(line[0])] = term_id_freqency

    return document_id



def sim(document_or_query, document):

    #document_or_query   [1,2,3]
    #document            {1:1,2:2,3:3}

    upper_sum = 0.0
    for term_id in document_or_query:
        upper_sum += document[term_id]

    document_sum = 0.0
    for term_id in document:
        document_sum += document[term_id] ** 2

    lower_sum = math.sqrt(document_sum) + math.sqrt(len(document_or_query))

    return upper_sum / lower_sum


def mmr(temp, document_term_vector, query_term_vector):
    #query_term_vector    [1,2,3]
    #document_term_vector {1:1,2:2,3:3}
    #temp [201 clueweb12-1700tw-11-11014, 201 clueweb12-1700tw-11-11014]

    for record in temp:
        

    return 0


if __name__ == '__main__':

    Query_document_Q1 = readTheFile_Query_document_Q1("../data/Q3/Q1answer.txt")
    document_term_vector = readTheFile_document_term_vector("../data/Q3/document_term_vectors.dat")
    query_term_vector = readTheFile_query_term_vector("../data/Q3/query_term_vectors.dat")
    print(document_term_vector)
    print(query_term_vector)
    print ((Query_document_Q1))
    count = 0
    for query_document_record_in_Q1 in Query_document_Q1:
        temp = []
        temp.append(query_document_record_in_Q1)
        count += 1
        index = int(query_document_record_in_Q1.split(" ")[0])
        if count % 100 == 0:
            mmr(temp, document_term_vector, query_term_vector[index])


