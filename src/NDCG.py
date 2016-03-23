from math import log2


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
            temp_dict = {}
            full_dict[line.split(" ")[0] + " " + line.split(" ")[2]] = int(line.split(" ")[3])
        return full_dict
        # print(full_dict)

# return the term_ids that appear in the file
def readTheFile_term(filename):
    with open(filename) as infile:
        return_value = {}
        for line in infile:
            return_value[(line.split(" ")[0])] = ""
    return return_value

# calculated the score of ndcg
def calculate_ndcg(term_id, k, term_docid, term_docid_rel_dict):
    rel_list = []

    # 241, 219 do not exist
    if int(term_id) < 219:
        start_index = 50 * (int(term_id) - 201)
    elif int(term_id) < 241 and int(term_id) > 219:
        start_index = 50 * (int(term_id) - 201 - 1)
    else:
        start_index = 50 * (int(term_id) - 201 - 2)

    end_index = start_index + k
    #print(start_index, end_index)
    for i in range (start_index, end_index):
        #print(term_docid[i])
        #print(term_docid_rel_dict.get(term_docid[i]))
        rel_list.append(term_docid_rel_dict.get(term_docid[i]))
    #print(rel_list)
    #return rel_list

    # I've got rel_list
    #print(rel_list)
    rel_list_sorted = sorted(rel_list, reverse=True)
    #print(rel_list_sorted)
    dcg_score = float(rel_list[0])
    idcg_score = float(rel_list_sorted[0])
    for index in range(1, k):
        dcg_score += (rel_list[index] / log2(index + 1))
    for index in range(1, k):
        idcg_score += (rel_list_sorted[index] / log2(index + 1))

    return dcg_score/idcg_score

if __name__ == '__main__':

    # output the data with (id + ranking + score)
    term_docid = readTheFile_dcg("../data/BM25b0.75_0.res")
    print(term_docid)
    #print(len(term_docid))

    # intput the data of Rel (str:int)
    term_docid_rel_dict = readTheFile_rel("../data/qrels.adhoc.txt")
    print(term_docid_rel_dict)

    #only the term id int
    term_dict = readTheFile_term("../data/BM25b0.75_0.res")
    print(term_dict)

    #Every Term
    #for term_id in term_dict:
        #print("Term:   " + str(term_id))
        #这里term_id 不是彻底的1-250 所以函数里面的 term_id-201会越界 因为会最后超出 只有2400个
        #for k in (50, 2):
    rel_list = calculate_ndcg(250, 5, term_docid, term_docid_rel_dict)





'''





'''
