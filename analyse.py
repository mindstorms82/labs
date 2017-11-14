#!/usr/bin/python3

import sys, getopt
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

def mysql_pred(cursor, cnx, table_name, lower_limit= 101, upper_limit= 116):
    result = []
    print(table_name)
    cursor.execute("SELECT `id`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for lene in cursor:
        if int(lower_limit) < lene[0] <= int(upper_limit):
            result.append((lene[1]))
    return result
## END Function ##

def mysql_true(cursor, cnx, table_name, lower_limit = 0, upper_limit = 0):
    result = []
    cursor.execute("SELECT COUNT(*) FROM `%s`", (table_name))
    cnx.commit()
    number_of_rows = cursor.fetchone()[0]
    cursor.execute("SELECT `id`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
    cnx.commit()
    for lene in cursor:
        if int(lower_limit) < lene[0] <= int(upper_limit):
            print("Row Nr.: ", lene[0])
            result.append((lene[1]))
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
    cursor.execute("SELECT `id`, `frame.len`, `tcp.port` FROM `%s`", (table_name))
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

def compare(table_name_true, table_name_pred, graphix=False):
    cursor, cnx = connect_db()
    match_list = []
    average_values = []
    maximum_values = []
    ticks = 15
    upper_limit = 0
    output = []
    output_persentage = []

    if graphix:
        for table in model_names:
            average_values.append(round(average_value(cursor,cnx, table)))
            #maximum_values.append(maximum_value(cursor, cnx, table))
        graph(cursor, cnx, average_values, min(average_values), max(average_values))

    max = get_maximum_input(cursor, cnx, table_name_true)
    packet_pred = mysql_pred(cursor, cnx, table_name_pred)

    for lower_limit in range(1, max, ticks):
        upper_limit = max if upper_limit > max else lower_limit + ticks
        packet_true = mysql_true(cursor, cnx, table_name_true, lower_limit, upper_limit)
        print(packet_pred)
        print(packet_true)
        output.append(jaccard_similarity_score(packet_true , packet_pred, normalize=False))
        output_persentage.append(jaccard_similarity_score(packet_true , packet_pred))

    print("Library name: ", table_name_true, "\n")
    #print("Length Range: ", (lower_limit, upper_limit))
    #print("Matches in totoal: " , output)
    print("Similarity in Persentage: " , (100 * max(output_persentage)))
## END Function ##


## Main Function ##
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1],"hi:",["ifile="])
    except getopt.GetoptError:
        print('analyse.py -i <inputfile>')
        sys.exit(2)
    compare(sys.argv[1], sys.argv[2])



