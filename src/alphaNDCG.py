from math import log2


# return the term_id and doc_id in order
def readTheFile_dcg_MMR(filename):
    term_rankging_score = []
    # read the idcg data
    with open(filename) as infile:
        for line in infile:
            term_rankging_score.append(line.split(" ")[0] + " " + line.split(" ")[4])
        return term_rankging_score


# return the term_id and doc_id and relevant rel_score
def readTheFile_rel(filename):
    with open(filename) as infile:
        full_dict = {}
        for line in infile:
            # str:int
            full_dict[line.split(" ")[0] + " " + line.split(" ")[2]] = int(line.split(" ")[3])
        return full_dict


def readTheFile_diversity_score(filename):
    with open(filename) as infile:
        full_dict = {}
        for line in infile:
            # str:int
            full_dict[line.split(" ")[0] + " " + line.split(" ")[2]] = int(line.split(" ")[1])
        return full_dict

# return the term_ids that appear in the file
def readTheFile_term(filename):
    with open(filename) as infile:
        return_value = {}
        for line in infile:
            return_value[int(line.split(" ")[0])] = ""
    return return_value


# calculated the score of ndcg
def calculate_ndcg_MMR(term_id, k, term_docid, term_docid_rel_dict, term_docid_diversity_score_dict):

    # alpha NDCG has parameters and one more list "term_docid_diversity_score_dict"
    alpha = 0.1


    # rel_list is the list that contains all the rel score value
    rel_list = []

    # The MMR one do not need to consider the term_id, because all of the term_id are listed in the list
    # So the start_index is begin with 0 if term_id is 201, while it will be 100 if the term_id is 202 (different from the BM25 one)
    start_index = 100 * (int(term_id) - 201)

    end_index = start_index + k

    for i in range(start_index, end_index):

        # That is the different between NDCG and alpha_NDCG, the score function
        if term_docid_rel_dict.get(term_docid[i]) is None:
            value = 0
        else:
            value = term_docid_rel_dict.get(term_docid[i]) * alpha + (1 - alpha) * term_docid_diversity_score_dict.get(term_docid[i])

        rel_list.append(value)

    #  rel_list_sorted is the sorted one, we used this list to calculate the IDCG part
    rel_list_sorted = sorted(rel_list, reverse=True)

    dcg_score = float(rel_list[0])
    idcg_score = float(rel_list_sorted[0])

    for index in range(1, k):
        dcg_score += (rel_list[index] / log2(index + 1))
    for index in range(1, k):
        idcg_score += (rel_list_sorted[index] / log2(index + 1))

    # print(dcg_score/idcg_score)
    if idcg_score == 0:
        return 0.0
    else:
        return dcg_score / idcg_score



# main function
if __name__ == '__main__':

    # intput the data of Rel (str:int)
    term_docid_rel_dict = readTheFile_rel("../data/Q5/qrels.ndeval.txt")

    # readTheFile_diversity_score
    term_docid_diversity_score_dict = readTheFile_diversity_score("../data/Q5/qrels.ndeval.txt")

    # MMR NDCG score
    # only the term id int
    term_dict = readTheFile_term("../data/Q5/MMR_0.25.txt")
    # output the data with (id + ranking + score)
    term_docid = readTheFile_dcg_MMR("../data/Q5/MMR_0.25.txt")

    # Portfolio NDCG score
    # only the term id int
    term_dict = readTheFile_term("../data/Q5/Portfolio_4.txt")
    # output the data with (id + ranking + score)
    term_docid = readTheFile_dcg_MMR("../data/Q5/Portfolio_4.txt")

    # The alpha NDCG is based on NDCG, while the score function is a little bit different
    # Add the comment to the Portfolio_4 one in order to output the result of MMR one

    # avg_ndcg_score is for saving the score of each alpha_NDCG
    avg_ndcg_score = [0.0] * 51

    # For Every Term
    for term_id in term_dict:
        # if you want to detailed data of each term_id, you should delete the comments below
        # print("")
        # print("Term:|   " + str(term_id))
        # print("K    |   NDCG@K")
        for k in (1, 5, 10, 20, 30, 40, 50):
            rel_list = calculate_ndcg_MMR(term_id, k, term_docid, term_docid_rel_dict, term_docid_diversity_score_dict)
            # only assign to the array that have k value
            avg_ndcg_score[k] += rel_list

    Denominator = 50
    alpha = 0.1
    print("MMR")
    print("lambda = 0.25")
    print("alpha  |K   |alpha - NDCG@K")
    print("%.1f    |1   |  %.2f" % (alpha, (avg_ndcg_score[1] / Denominator)))
    print("%.1f    |5   |  %.2f" % (alpha, (avg_ndcg_score[5] / Denominator)))
    print("%.1f    |10  |  %.2f" % (alpha, (avg_ndcg_score[10] / Denominator)))
    print("%.1f    |20  |  %.2f" % (alpha, (avg_ndcg_score[20] / Denominator)))
    print("%.1f    |30  |  %.2f" % (alpha, (avg_ndcg_score[30] / Denominator)))
    print("%.1f    |40  |  %.2f" % (alpha, (avg_ndcg_score[40] / Denominator)))
    print("%.1f    |50  |  %.2f" % (alpha, (avg_ndcg_score[50] / Denominator)))
