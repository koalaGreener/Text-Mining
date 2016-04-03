# maximal marginal relevance (MMR)
import math
from scipy.linalg import norm


def readTheFile_Query_document_Q1(filename):
    qurey_document = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            qurey_document.append(line.split(" ")[0] + " " + line.split(" ")[2])
        return qurey_document


def readTheFile_query_term_vector(filename):
    query_id = dict()
    with open(filename) as infile:
        for line in infile:
            term_id_freqency = dict()
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                term_id_freqency[int(line[i].split(":")[0])] = int(line[i].split(":")[1])
                query_id[int(line[0])] = term_id_freqency

    return query_id


def readTheFile_document_term_vector(filename):
    document_id = dict()
    with open(filename) as infile:
        for line in infile:
            term_id_freqency = dict()
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                term_id_freqency[int(line[i].split(":")[0])] = int(line[i].split(":")[1])
                document_id[(line[0])] = term_id_freqency

    return document_id


def sim(document_or_query, document):  # {} {}

    # document_or_query   {1:1,2:100,4:500}
    # document            {1:1,2:2,3:3}

    upper_sum = 0.0
    lower_query_or_document_sum = 0.0
    lower_document_sum = 0.0

    for term_id in document_or_query:
        lower_query_or_document_sum += (document_or_query[term_id] ** 2)
        if term_id in document:
            upper_sum += (document[term_id] * document_or_query[term_id])

    for term_id in document:
        lower_document_sum += (document[term_id] ** 2)

    lower_sum = math.sqrt(lower_document_sum * lower_query_or_document_sum)

    return upper_sum / lower_sum

def mmr(mmr_query_id, temp, document_term_vector, query_term_vector):  # [] {} {}
    # temp [201 clueweb12-1700tw-11-11014, 201 clueweb12-1700tw-11-11014]
    # document_term_vector { clueweb12-1700tw-11-11014: {1:1,2:2,3:3}}
    # query_term_vector    {1:1,2:1,3:1}
    lambda2 = 0.5
    lambda1 = 0.25
    # query_term_vector  -> q
    D = dict()  # 全部记录在案的 doc_id 100个
    Dq = dict()  # 那个不断放进去的
    chosen_score = 0.0
    chosen_document_id = ''

    for record in temp:
        D[record.split(" ")[1]] = 0

    #print(len(D))
    #print(Dq)
    #print(D)
    # initial
    for document_id in D:
        # score = Calculate_mmr(query_term_vector, document_term_vector[document_id], Dq)
        score = 0.25 * sim(query_term_vector, document_term_vector[document_id])
        if score > chosen_score:
            chosen_score = score
            chosen_document_id = document_id

    print("%d  q0  %s   1  %.7f" % (mmr_query_id, chosen_document_id, chosen_score))


    Dq[chosen_document_id] = 0
    del D[chosen_document_id]
    #print(Dq)
    #print(D)
    #print(first_mmr_value)

    # 双重循环
    chosen_Dj = []

    ranking = 1
    for i in range(1, 100):
        chosen_d = ''
        chosen_score = - 9999.0
        for candidate_d in D:
            temp = sim(query_term_vector, document_term_vector[candidate_d])
            for candidate_Dj in Dq:
                score = lambda1 * temp - ((1 - lambda1) * sim(document_term_vector[candidate_d], document_term_vector[candidate_Dj]))
                if score > chosen_score:
                    chosen_d = candidate_d
                    chosen_score = score

        #print(D)
        #print(Dq)
        #print(chosen_d)
        #print(chosen_score)
        Dq[chosen_d] = 0
        del D[chosen_d]
        ranking += 1
        print("%d  q0  %s  %2d  %.7f" % (mmr_query_id, chosen_d, ranking, chosen_score))


if __name__ == '__main__':


    Query_document_Q1 = readTheFile_Query_document_Q1("../data/Q3/Q1answer.txt")
    document_term_vector = readTheFile_document_term_vector("../data/Q3/document_term_vectors.dat")
    query_term_vector = readTheFile_query_term_vector("../data/Q3/query_term_vectors.dat")
    # print(document_term_vector)
    # print(query_term_vector)
    # print (len(Query_document_Q1))

    count = 0
    temp = dict()
    for query_document_record_in_Q1 in Query_document_Q1:
        temp[query_document_record_in_Q1] = 0
        count += 1
        if count % 100 == 0:
            index = int(query_document_record_in_Q1.split(" ")[0])
            #profile.run("mmr(int(200 + count/100), temp, document_term_vector, query_term_vector[index])")
            #break
            mmr(int(200 + count/100), temp, document_term_vector, query_term_vector[index])
            temp = dict()
            #print("----")
