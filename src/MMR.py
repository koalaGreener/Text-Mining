# maximal marginal relevance (MMR)
import math


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
            term_id_freqency = {}
            line = line.strip(" \n")
            line = line.split(" ")
            for i in range(1, len(line)):
                term_id_freqency[int(line[i].split(":")[0])] = int(line[i].split(":")[1])
                query_id[int(line[0])] = term_id_freqency

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


def sim(document_or_query, document):  # {} {}

    # document_or_query   {1:1,2:1,4:1}
    # document            {1:1,2:2,3:3}

    upper_sum = 0.0
    for term_id in document_or_query:
        if document.get(term_id) is not None:
            upper_sum += document[term_id]

    document_sum = 0.0
    for term_id in document:
        document_sum += document[term_id] ** 2

    lower_sum = math.sqrt(document_sum) + math.sqrt(len(document_or_query))
    # print(document_or_query)
    # print(len(document_or_query))
    return upper_sum / lower_sum


def mmr(temp, document_term_vector, query_term_vector):  # [] {} {}
    # temp [201 clueweb12-1700tw-11-11014, 201 clueweb12-1700tw-11-11014]
    # document_term_vector { clueweb12-1700tw-11-11014: {1:1,2:2,3:3}}
    # query_term_vector    {1:1,2:1,3:1}

    # query_term_vector  -> q
    D = []  # 全部记录在案的 doc_id 100个
    Dq = []  # 那个不断放进去的
    mmr_query_id = 0
    chosen_score = 0.0
    chosen_document_id = ''
    first_mmr_value = 0.0
    for record in temp:
        D.append(record.split(" ")[1])
        mmr_query_id = record.split(" ")[0]

    #print(len(D))

    #print(Dq)
    #print(D)
    # initial
    for document_id in D:
        # score = Calculate_mmr(query_term_vector, document_term_vector[document_id], Dq)
        score = sim(query_term_vector, document_term_vector[document_id])
        first_mmr_value = score * 0.5
        if score > chosen_score:
            chosen_score = score
            chosen_document_id = document_id

    print(str(mmr_query_id) + "   q0    " + str(chosen_document_id) + "  " + "1" + "    " + str(chosen_score) + "      mmr")

    Dq.append(chosen_document_id)
    D.remove(chosen_document_id)

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
            for candidate_Dj in Dq:
                score = Calculate_mmr(query_term_vector, document_term_vector[candidate_d], document_term_vector[candidate_Dj])
                #print(score)
                if score > chosen_score:
                    chosen_d = candidate_d
                    chosen_score = score

        #print(D)
        #print(Dq)
        #print(chosen_d)
        #print(chosen_score)
        Dq.append(chosen_d)
        D.remove(chosen_d)
        ranking += 1
        print( str(mmr_query_id) + "   q0    " + chosen_d + "  " + str(ranking) + "    " + str(chosen_score) + "    mmr")
        #print("--")



def Calculate_mmr(q, d, dj):  # {} {} {}
    lambda1 = 0.5
    lambda2 = 0.25
    return lambda1 * sim(q, d) - ((1 - lambda1) * sim(d, dj))


if __name__ == '__main__':

    Query_document_Q1 = readTheFile_Query_document_Q1("../data/Q3/Q1answer.txt")
    document_term_vector = readTheFile_document_term_vector("../data/Q3/document_term_vectors.dat")
    query_term_vector = readTheFile_query_term_vector("../data/Q3/query_term_vectors.dat")
    # print(document_term_vector)
    # print(query_term_vector)
    # print ((Query_document_Q1))

    count = 0
    temp = []
    for query_document_record_in_Q1 in Query_document_Q1:
        temp.append(query_document_record_in_Q1)
        count += 1
        index = int(query_document_record_in_Q1.split(" ")[0])
        if count % 100 == 0:
            mmr(temp, document_term_vector, query_term_vector[index])
            #print("----")
