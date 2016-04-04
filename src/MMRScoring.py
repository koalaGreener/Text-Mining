# maximal marginal relevance (MMR)
import math

# read the BM25 file from Q1
# return the [Query_id document_id]
def readTheFile_Query_document_Q1(filename):
    qurey_document = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            qurey_document.append(line.split(" ")[0] + " " + line.split(" ")[2])
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

# calculate the cosine similarity of two document or one query one document
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

# Use the mmr function to calculate the mmr score
def mmr(mmr_query_id, temp, document_term_vector, query_term_vector):  # [] {} {}
    # temp [201 clueweb12-1700tw-11-11014, 201 clueweb12-1700tw-11-11014]
    # document_term_vector { clueweb12-1700tw-11-11014: {1:1,2:2,3:3}}
    # query_term_vector    {1:1,2:1,3:1}

    # Parameters
    lambda1 = 0.5
    lambda2 = 0.25
    # query_term_vector  -> q
    D = dict()  # The D dcit included all of the doc_id, 100 doc_id
    Dq = dict()  # The Dq dict is empty at the very beginning
    chosen_score = 0.0
    chosen_document_id = ''

    # import all the document_id into D
    for record in temp:
        D[record.split(" ")[1]] = 0


    # For the first one, we need to calculate the score manually
    for document_id in D:
        # score = Calculate_mmr(query_term_vector, document_term_vector[document_id], Dq)
        score = 0.25 * sim(query_term_vector, document_term_vector[document_id])
        if score > chosen_score:
            chosen_score = score
            chosen_document_id = document_id

    print("%d  q0  %s   1  %.7f" % (mmr_query_id, chosen_document_id, chosen_score))

    # Add the chosen_document_id into Dq and then remove it from D
    Dq[chosen_document_id] = 0
    del D[chosen_document_id]

    # Then we will calculate the rest of the 99 score.
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

        # Add the chosen_document_id into Dq and then remove it from D
        Dq[chosen_d] = 0
        del D[chosen_d]

        #output the formatted data
        ranking += 1
        print("%d  q0  %s  %2d  %.7f" % (mmr_query_id, chosen_d, ranking, chosen_score))





######################################## # main function Started here ################################################
if __name__ == '__main__':

    # read the data
    Query_document_Q1 = readTheFile_Query_document_Q1("../data/Q3/Q1answer.txt")
    # return the {document_id {1:2}, document_id {1:2}}
    document_term_vector = readTheFile_document_term_vector("../data/Q3/document_term_vectors.dat")
    query_term_vector = readTheFile_query_term_vector("../data/Q3/query_term_vectors.dat")

    # Use the count to call the mmr when data reached a fixed value, and the data will store in Q1_sequence dictionary
    count = 0
    Q1_sequence = dict()

    # iteration of all the record in Query_document_Q1
    for query_document_record_in_Q1 in Query_document_Q1:
        Q1_sequence[query_document_record_in_Q1] = 0
        count += 1
        # For every 100 data, we will use the MMR to calculate the score, because every 100 data the term_id changed (201 -> 202 -> 203)
        if count % 100 == 0:
            # find out what exactly t he term_id is, such as 201, 202
            index = int(query_document_record_in_Q1.split(" ")[0])
            # Used the mmr function to calculate the score
            mmr(int(200 + count/100), Q1_sequence, document_term_vector, query_term_vector[index])
            # clear the dictionary
            temp = dict()
