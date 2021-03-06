from math import log2


# return the term_id and doc_id in order
# That is for MMR and Portfolio
def readTheFile_dcg_MMR(filename):
    term_rankging_score = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            term_rankging_score.append(line.split(" ")[0] + " " + line.split(" ")[4])
        return term_rankging_score


# return the term_id and doc_id in order
def readTheFile_dcg(filename):
    term_rankging_score = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            if int(line.split(" ")[3]) < 50:
                term_rankging_score.append(line.split(" ")[0] + " " + line.split(" ")[2])
        return term_rankging_score


# return the term_id and doc_id and relevant rel_score
def readTheFile_rel(filename):
    with open(filename) as infile:
        full_dict = {}
        for line in infile:
            # str:int
            #
            if int(line.split(" ")[3]) == -2:
                full_dict[line.split(" ")[0] + " " + line.split(" ")[2]] = 0
            else:
                full_dict[line.split(" ")[0] + " " + line.split(" ")[2]] = int(line.split(" ")[3])
        return full_dict


# return the term_ids that appear in the file
def readTheFile_term(filename):
    with open(filename) as infile:
        return_value = {}
        for line in infile:
            return_value[int(line.split(" ")[0])] = ""
    return return_value


# calculated the score of ndcg
# That is for MMR and Portfolio
def calculate_ndcg_MMR(term_id, k, term_docid, term_docid_rel_dict):
    rel_list = []

    # The MMR one do not need to consider the term_id, because all of the term_id are listed in the list
    start_index = 50 * (int(term_id) - 201)

    end_index = start_index + k
    for i in range(start_index, end_index):
        # print(term_docid[i])
        # print(term_docid_rel_dict.get(term_docid[i]))
        value = term_docid_rel_dict.get(term_docid[i])
        if value is None:
            rel_list.append(0)
        else:
            rel_list.append(value)

    # I've got rel_list
    rel_list_sorted = sorted(rel_list, reverse=True)

    dcg_score = float(rel_list[0])
    idcg_score = float(rel_list_sorted[0])
    for index in range(1, k):
        dcg_score += (rel_list[index] / log2(index + 1))
    for index in range(1, k):
        idcg_score += (rel_list_sorted[index] / log2(index + 1))

    if idcg_score == 0:
        return 0.0
    else:
        return dcg_score / idcg_score


# calculated the score of ndcg
def calculate_ndcg(term_id, k, term_docid, term_docid_rel_dict):
    rel_list = []

    # 241, 219 term_id do not exist
    if int(term_id) < 219:
        start_index = 50 * (int(term_id) - 201)
    elif int(term_id) < 241 and int(term_id) > 219:
        start_index = 50 * (int(term_id) - 201 - 1)
    else:
        start_index = 50 * (int(term_id) - 201 - 2)

    end_index = start_index + k
    # print(start_index, end_index)
    for i in range(start_index, end_index):
        # print(term_docid[i])
        # print(term_docid_rel_dict.get(term_docid[i]))
        value = term_docid_rel_dict.get(term_docid[i])
        if value is None:
            rel_list.append(0)
        else:
            rel_list.append(value)

    # I've got rel_list
    rel_list_sorted = sorted(rel_list, reverse=True)

    dcg_score = float(rel_list[0])
    idcg_score = float(rel_list_sorted[0])
    for index in range(1, k):
        dcg_score += (rel_list[index] / log2(index + 1))
    for index in range(1, k):
        idcg_score += (rel_list_sorted[index] / log2(index + 1))

    if idcg_score == 0:
        return 0.0
    else:
        return dcg_score / idcg_score


######################################## # main function Started here ################################################
# main function
if __name__ == '__main__':

    # output the data with (id + ranking + score)
    term_docid = readTheFile_dcg("../data/Q2/BM25b0.75_0.res")
    # print(term_docid)
    # print(len(term_docid))

    # intput the data of Rel (str:int)
    term_docid_rel_dict = readTheFile_rel("../data/Q2/qrels.adhoc.txt")
    # print(term_docid_rel_dict)

    # only the term id int
    term_dict = readTheFile_term("../data/Q2/BM25b0.75_0.res")
    # print(term_dict)


    ######################################### The result depends on the input data ################################################
    # The default one is BM25, but if we import the MMR or Portfolio data, we can also calculate the value
    # You should notice that the  "readTheFile_dcg_MMR" function is different from the "readTheFile_dcg"
    # While the "    readTheFile_rel" and "    readTheFile_term"  is still the same


    ##### If you want to see the NDCG score of MMR or Portfolio, delete the comment line

    # MMR NDCG score
    #term_dict = readTheFile_term("../output/Q3/MMR_0.5.txt")
    #term_docid = readTheFile_dcg_MMR("../output/Q3/MMR_0.5.txt")

    # Portfolio NDCG score
    #term_dict = readTheFile_term("../output/Q4/Portfolio_4.txt")
    #term_docid = readTheFile_dcg_MMR("../output/Q4/Portfolio_4.txt")

    # Every Term
    avg_ndcg_score = [0.0] * 51
    for term_id in term_dict:
        # if you want to detailed data of each term_id, you should delete the comments below
        # print("")
        # print("Term:|   " + str(term_id))
        # print("K    |   NDCG@K")
        for k in (1, 5, 10, 20, 30, 40, 50):
            rel_list = calculate_ndcg(term_id, k, term_docid, term_docid_rel_dict)
            #rel_list = calculate_ndcg_MMR(term_id, k, term_docid, term_docid_rel_dict)

            # only assign to the array that have k value
            avg_ndcg_score[k] += rel_list

    #The BM25 one did not have two term_id, so the length should be 48
    Denominator_BM25 = 48
    Denominator_MMR = 50
    Denominator = Denominator_BM25
    print("bm25")
    print("1    |   %.2f" % (avg_ndcg_score[1]  / Denominator))
    print("5    |   %.2f" % (avg_ndcg_score[5]  / Denominator))
    print("10   |   %.2f" % (avg_ndcg_score[10] / Denominator))
    print("20   |   %.2f" % (avg_ndcg_score[20] / Denominator))
    print("30   |   %.2f" % (avg_ndcg_score[30] / Denominator))
    print("40   |   %.2f" % (avg_ndcg_score[40] / Denominator))
    print("50   |   %.2f" % (avg_ndcg_score[50] / Denominator))
