# maximal marginal relevance (MMR)
import math


# read the BM25 file from Q1
# return the [Query_id document_id]
def readTheFile_Query_document_Q1(filename):
    qurey_document = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            qurey_document.append(line.split(" ")[0] + " " + line.split(" ")[2]+ " " + line.split(" ")[3]+ " " + line.split(" ")[4])
        return qurey_document

# read the query
# return the {query_id {1:2}, query_id {1:2}}
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

# Almost the same as "readTheFile_query_term_vector"
# return the same format data but the key is document_id
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



# Calculate the Pd,dj value, it will be used when calculated the Portfolio score
def Pddj(d, dj):  # {} {}

    # d   {1:1,2:100,4:500}
    # dj  {1:1,2:100,4:500}

    #Fulfill the Set, the set contains all of the term_id that appear in both d and dj, like a union
    complete_set = set()
    for term_id in d:
        complete_set.add(term_id)
    for term_id in dj:
        complete_set.add(term_id)

    length_complete_set = len(complete_set)

    #Calculate the Mean of d and dj
    mean_d = 0.0
    mean_dj = 0.0
    for term_id in d:
        mean_d += d[term_id]
    mean_d /= length_complete_set

    for term_id in dj:
        mean_dj += dj[term_id]
    mean_dj /= length_complete_set

    # calculated the Numerator part
    # calculated the denominator part
    Numerator = 0.0
    denominator_left = 0.0
    denominator_right = 0.0
    for term_id in complete_set:
        Numerator += (d.get(term_id, 0) - mean_d ) * (dj.get(term_id, 0) - mean_dj )
        denominator_left += (d.get(term_id, 0) - mean_d ) ** 2
        denominator_right += (dj.get(term_id, 0) - mean_dj ) ** 2

    return Numerator / math.sqrt(denominator_left * denominator_right)



def portfolio(mmr_query_id, Q1_sequence, document_term_vector):  # [] {}
    # Q1_sequence [201 clueweb12-1700tw-11-11014, 201 clueweb12-1700tw-11-11014]
    # document_term_vector { clueweb12-1700tw-11-11014: {1:1,2:2,3:3}}
    b2 = 4.0
    b1 = -4.0
    # query_term_vector  -> q
    D = dict()  # doc_id * 100 are all in D dict
    D_ranking = dict()  # the relvant ranking are also put in D_ranking dict
    Dq = []  # whenever the D remove the element, then add it into the Dq

    for record in Q1_sequence:
        D[record.split(" ")[1]] = float(record.split(" ")[3])
        D_ranking[record.split(" ")[1]] = int(record.split(" ")[2])

    # The first ranking element is the BM25 1st one, so we simply manually print the result
    chosen_document_id = Q1_sequence[0].split(" ")[1]

    print("%d  q0  %s   %3d  %.7f" % (mmr_query_id, chosen_document_id, 1, D[chosen_document_id] - b1 * (1 / (D_ranking[chosen_document_id] + 1))))
    del D[chosen_document_id]
    chosen_score = -999.0
    chosen_document_id = ''

    # iterations for calculated the rest of score
    for i in range(1, 100):
        for document_id in D:

            # the sum_value is the part of the score function
            sum_value = 0
            for j in range(1, len(Dq) + 1):
                sum_value += (1 / pow(2, j)) * Pddj(document_term_vector[document_id], document_term_vector[Dq[j - 1]])
            # that's the score function of Portfolio ranking
            score = D[document_id] - b1 * (1 / (D_ranking[document_id] + 1) ) - 2 * b1 * sum_value

            # Only memorize the largest score and it's document id
            if score > chosen_score:
                chosen_score = score
                chosen_document_id = document_id

        # Add it into Dq dict and remove it from D dcit
        Dq.append(chosen_document_id)
        del D[chosen_document_id]
        print("%d  q0  %s   %3d  %.7f" % (mmr_query_id, chosen_document_id, i + 1, chosen_score))
        # reset the score for every iteraion
        chosen_score = -999.0


######################################## # main function Started here ################################################

if __name__ == '__main__':

    # return ['201 clueweb12-0905wb-50-14578 0 16.702539979527295'.....]
    Query_document_Q1 = readTheFile_Query_document_Q1("../data/Q4/Q1answer.txt")
    # return the {document_id {1:2}, document_id {1:2}}
    document_term_vector = readTheFile_document_term_vector("../data/Q4/document_term_vectors.dat")

    count = 0
    # used the Q1_sequence to store every 100 data and calculate their portfolio score
    Q1_sequence = []
    for query_document_record_in_Q1 in Query_document_Q1:
        Q1_sequence.append(query_document_record_in_Q1)
        count += 1
        if count % 100 == 0:
            # The index should be 201,202,....
            index = int(query_document_record_in_Q1.split(" ")[0])
            portfolio(int(200 + count/100), Q1_sequence, document_term_vector)
            #reset the Q1_sequence
            Q1_sequence = []
