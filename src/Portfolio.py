# maximal marginal relevance (MMR)
import math


def readTheFile_Query_document_Q1(filename):
    qurey_document = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            qurey_document.append(line.split(" ")[0] + " " + line.split(" ")[2]+ " " + line.split(" ")[3]+ " " + line.split(" ")[4])
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


def eddj(d, dj):  # {} {}

    # d   {1:1,2:100,4:500}
    # dj  {1:1,2:100,4:500}

    #先来个完整的 set
    complete_set = set()
    for term_id in d:
        complete_set.add(term_id)
    for term_id in dj:
        complete_set.add(term_id)

    length_complete_set = len(complete_set)

    #再算一下 Mean 的值
    mean_d = 0.0
    mean_dj = 0.0
    for term_id in d:
        mean_d += d[term_id]
    mean_d /= length_complete_set

    for term_id in dj:
        mean_dj += dj[term_id]
    mean_dj /= length_complete_set

    # 先求一下分子好了
    # 再求一下分母好了
    fenzi = 0.0
    fenmu_left = 0.0
    fenmu_right = 0.0
    for term_id in complete_set:
        fenzi += (d.get(term_id, 0) - mean_d ) * (dj.get(term_id, 0) - mean_dj )
        fenmu_left += (d.get(term_id, 0) - mean_d ) ** 2
        fenmu_right += (dj.get(term_id, 0) - mean_dj ) ** 2

    return fenzi / math.sqrt(fenmu_left * fenmu_right)



def portfolio(mmr_query_id, Q1_sequence, document_term_vector):  # [] {}
    # temp [201 clueweb12-1700tw-11-11014, 201 clueweb12-1700tw-11-11014]
    # document_term_vector { clueweb12-1700tw-11-11014: {1:1,2:2,3:3}}
    b1 = 4.0
    b2 = -4.0
    # query_term_vector  -> q
    D = dict()  # 全部记录在案的 doc_id 100个
    D_ranking = dict()  # 对应的 ranking
    Dq = []  # 那个不断放进去的List

    for record in Q1_sequence:
        D[record.split(" ")[1]] = float(record.split(" ")[3])
        D_ranking[record.split(" ")[1]] = int(record.split(" ")[2])

    chosen_document_id = Q1_sequence[0].split(" ")[1]

    print("%d  q0  %s   %3d  %.7f" % (mmr_query_id, chosen_document_id, 1, D[chosen_document_id] - 4.0 * (1 / (D_ranking[chosen_document_id] + 1))))
    del D[chosen_document_id]
    chosen_score = -999.0
    chosen_document_id = ''
    #print(len(D))
    #print(len(Dq))
    #print(Dq)
    #print(D)

    # iterations
    for i in range(1, 100):
        for document_id in D:

            sum_value = 0
            for j in range(1, len(Dq) + 1):
                #print(j)
                sum_value += (1 / pow(2, j)) * eddj(document_term_vector[document_id], document_term_vector[Dq[j - 1]])

            score = D[document_id] - 4.0 * (1 / (D_ranking[document_id] + 1) ) - 8.0 * sum_value
            if score > chosen_score:
                chosen_score = score
                chosen_document_id = document_id

        Dq.append(chosen_document_id)
        del D[chosen_document_id]
        print("%d  q0  %s   %3d  %.7f" % (mmr_query_id, chosen_document_id, i + 1, chosen_score))
        chosen_score = -999.0


    #print(Dq)
    #print(D)
    #print(first_mmr_value)


if __name__ == '__main__':


    Query_document_Q1 = readTheFile_Query_document_Q1("../data/Q4/Q1answer.txt")
    document_term_vector = readTheFile_document_term_vector("../data/Q4/document_term_vectors.dat")
    #query_term_vector = readTheFile_query_term_vector("../data/Q4/query_term_vectors.dat")
    # print(document_term_vector)
    # print(query_term_vector)
    #print ((Query_document_Q1))

    count = 0
    Q1_sequence = []
    for query_document_record_in_Q1 in Query_document_Q1:
        Q1_sequence.append(query_document_record_in_Q1)
        count += 1
        if count % 100 == 0:
            index = int(query_document_record_in_Q1.split(" ")[0])
            portfolio(int(200 + count/100), Q1_sequence, document_term_vector)
            Q1_sequence = []
