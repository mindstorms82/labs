#!/usr/bin/python3

import sys, time, getopt
import numpy as np
from sklearn.metrics import jaccard_similarity_score
from msql import connect_db
import matplotlib.pyplot as plt

## Global lists ##
model_names = (
'facebook',

    'ebay',
    'skype',
    'youtube'
 )

def mysql_pred(cursor, cnx, table_name, lower_limit = 100, upper_limit= 120):
    result = []
    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for len in cursor:
        if int(lower_limit) <= len[0] <= int(upper_limit):
            result.append((len[1]))
    return result
## END Function ##

def mysql_true(cursor, cnx, table_name, lower_limit = 0, upper_limit = 0):
    print(table_name)
    result = []
    cursor.execute("SELECT COUNT(*) FROM `%s`", (table_name))
    cnx.commit()
    number_of_rows = cursor.fetchone()[0]

    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for len in cursor:
        if int(lower_limit) <= len[0] <= int(upper_limit):
            result.append((len[1]))
    return result
## END Function ##

def average_value(cursor, cnx, table_name):
    result=[]
    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for lene in cursor:
        result.append(lene[1])
    average = sum(result) / len(result)
    return average
## END Function ##

def maximum_value(cursor, cnx, table_name):
    result=[]
    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for lene in cursor:
        result.append(lene[1])
    return max(result)
## END Function ##

def get_maximum_input(cursor, cnx, table_name):
    cursor.execute("SELECT COUNT(*) FROM `%s`", (table_name))
    cnx.commit()
    number_of_rows = cursor.fetchone()[0]
    return  number_of_rows
## END Function ##

def graph(cursor, cnx, values, lower_limit, upper_limit):
    x_pos = np.arange(len(model_names))
    fig, ax = plt.subplots(figsize=(3,11))
    ax.grid(True)
    ax.set_title('Average Packet Size')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(model_names, rotation='horizontal')
    ax.set_ylabel('Packet length')
    ax.set_ylim((lower_limit * 0.1), (upper_limit + 400))
    ax.bar(x_pos, values, alpha=0.5, color=['b'])
    ax.minorticks_on()
    plt.tight_layout()
    plt.show()
## END Function ##

def test():
    ticks = 11
    j = 0
    i = 0
    for i in range(1, 50, ticks):
        j = j + 11
        print(i, j)


def compare(table_name_true, table_name_pred, graphix=False):
    cursor, cnx = connect_db()
    match_list = []

    if graphix:
        average_values = []
        maximum_values = []
        for table in model_names:
            average_values.append(round(average_value(cursor,cnx, table)))
            #maximum_values.append(maximum_value(cursor, cnx, table))
        graph(cursor, cnx, average_values, min(average_values), max(average_values))

    max = get_maximum_input(cursor, cnx, table_name_true)
    ticks = 11
    packet_pred = mysql_pred(cursor, cnx, table_name_pred)
    for lower_limit in range(1, max, ticks):
        #upper_limit = lower_limit + ticks
        upper_limit = max if upper_limit > max else lower_limit + ticks
        packet_true = mysql_true(cursor, cnx, table_name_true, lower_limit, upper_limit)

        #if len(skype_pred) > len(skype_true):
        #    skype_pred = skype_pred[0:len(skype_true)]
        #elif len(skype_true) > len(skype_pred):
        #    skype_true = skype_true[0:len(skype_pred)]

        output = jaccard_similarity_score(packet_true , packet_pred, normalize=False)
        output_persentage = jaccard_similarity_score(packet_true , packet_pred)
        print("Library name: ", table_name_true, "\n")
        print("Length Range: %s - %s", (lower_limit, upper_limit))
        print("Matches in totoal: " , output)
        print("Matches in Persentage: " , (100 * output_persentage))
## END Function ##




## Main Function ##
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1],"hi:",["ifile="])
    except getopt.GetoptError:
        print('analyse.py -i <inputfile>')
        sys.exit(2)

    test()
    exit(0)
    compare(sys.argv[1], sys.argv[2])
    #compare("facebook", sys.argv[2])
    #compare("youtube", sys.argv[2])
    #compare("skype", sys.argv[2])




