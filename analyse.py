#!/usr/bin/python3

import sys, time, getopt
import numpy as np
from sklearn.metrics import jaccard_similarity_score
from msql import connect_db

def mysql_pred(cursor, cnx, table_name):
    print(table_name)
    result = []
    #cursor.execute("SELECT * FROM `%s` WHERE `frame.len` >= 300", (table_name_true))
    #cursor.execute("SELECT `frame.len` FROM `%s`", (table_name))
    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for len in cursor:
        if 190 <= len[0] <= 200:
            result.append((len[1]))
    return result

def mysql_true(cursor, cnx, table_name):
    print(table_name)
    result = []
    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for len in cursor:
        print(len(cursor))
        if  190 <= len[0] <= 200:
            result.append((len[1]))
    return result


def compare(table_name_true, table_name_pred):
    cursor, cnx = connect_db()
    skype_true = mysql_true(cursor, cnx, table_name_true)
    skype_pred = mysql_pred(cursor, cnx, table_name_pred)

    if len(skype_pred) > len(skype_true):
        skype_pred = skype_pred[0:len(skype_true)]
    elif len(skype_true) > len(skype_pred):
        skype_true = skype_true[0:len(skype_pred)]

    output = jaccard_similarity_score(skype_true, skype_pred, normalize=False)
    output_persentage = jaccard_similarity_score(skype_true, skype_pred)
    print("Library name: ", table_name_true, "\n")
    print("Matches in totoal: " , output)
    print("Matches in Persentage: " , (100 * output_persentage))






if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1],"hi:",["ifile="])
    except getopt.GetoptError:
        print('analyse.py -i <inputfile>')
        sys.exit(2)
    compare(sys.argv[1], sys.argv[2])
    #compare("facebook", sys.argv[2])
    #compare("youtube", sys.argv[2])
    #compare("skype", sys.argv[2])




