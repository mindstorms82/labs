#!/usr/bin/python3

import sys, getopt
import numpy as np
from sklearn.metrics import jaccard_similarity_score
from msql import connect_db
import matplotlib.pyplot as plt

## Global lists ##

## Main list ##
model_names = (
    'facebook',
    'ebay',
    'skype',
    'youtube'
 )

## lite is a modified version of model_names for more performance ##
model_names_lite = (
    'facebook_lite',
    'ebay_lite',
    'skype',
    'youtube_lite'
 )

## Debug List ##
model_names_debug = (
    'skype_clone',
    'skype_clone',
    'skype_clone',
    'skype_clone'
)

lower_range = 836
upper_range = 846

def mysql_pred(cursor, cnx, table_name, lower_limit= lower_range, upper_limit= upper_range):
    result = []
    cursor.execute("SELECT `id`, `frame.len`, `tcp.flags` FROM `%s`", (table_name))
    cnx.commit()
    for lene in cursor:
        if int(lower_limit) < lene[0] <= int(upper_limit):
            #hex_to_int = int(str(lene[2]), 0)
            result.append(lene[1])
    return result
## END Function ##

def mysql_true(cursor, cnx, table_name, lower_limit = 0, upper_limit = 0):
    result = []
    cursor.execute("SELECT `id`, `frame.len`, `tcp.flags` FROM `%s`", (table_name))
    cnx.commit()
    for lene in cursor:
        if int(lower_limit) < lene[0] <= int(upper_limit):
            #hex_to_int = int(str(lene[2]), 0)
            result.append(lene[1])
    return result
## END Function ##

def average_value(cursor, cnx, table_name):
    result=[]
    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.flags` FROM `%s`", (table_name))
    cnx.commit()
    for lene in cursor:
        result.append(lene[1])
    average = sum(result) / len(result)
    return average
## END Function ##

def maximum_value(cursor, cnx, table_name):
    result=[]
    cursor.execute("SELECT `id`, `frame.len`, `tcp.flags` FROM `%s`", (table_name))
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

def graph(values, plot_name,lower_limit, upper_limit):
    x_pos = np.arange(len(model_names))
    fig, ax = plt.subplots(figsize=(3,11))
    ax.grid(True)
    ax.set_title('Web Applications Likelihood')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(model_names, rotation='horizontal')
    ax.set_ylabel(plot_name)
    #ax.set_ylim((lower_limit * 0.1), (upper_limit + 100))
    ax.set_ylim((lower_limit * 0.1), (100))
    ax.bar(x_pos, values, alpha=0.5, color=['b'])
    ax.minorticks_on()
    plt.tight_layout()
    plt.show()
## END Function ##

def compare(table_name_true, table_name_pred, graphix=False):
    cursor, cnx = connect_db()
    average_values = []
    ticks = upper_range - lower_range
    upper_limit = 0
    output_percentage = []

    if graphix:
        for table in model_names:
            average_values.append(round(average_value(cursor,cnx, table)))
        graph(average_values, 'Packet_length',min(average_values), max(average_values))

    max = get_maximum_input(cursor, cnx, table_name_true)
    packet_pred = mysql_pred(cursor, cnx, table_name_pred)
    print(packet_pred)

    for lower_limit in range(1, max, ticks):
        upper_limit = max if upper_limit > max else lower_limit + ticks
        packet_true = mysql_true(cursor, cnx, table_name_true, lower_limit, upper_limit)
        if len(packet_true) != len(packet_pred):
            packet_pred = packet_pred[0:len(packet_true)]
        output_percentage.append(jaccard_similarity_score(packet_true , packet_pred))

    tmp = outputo(output_percentage)
    tmp = tmp * 100
    print("Library name: ", table_name_true, "\n")
    return tmp
## END Function ##

def outputo(ls):
    tmp = ls[:]
    return max(tmp)

def plot_similar():
    values_internal = []
    for module in model_names_lite:
        values_internal.append(compare(module, 'alexa'))

    print(values_internal)
    graph(values_internal, 'Packet Similarity',min(values_internal), max(values_internal))

## Main Function ##
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1],"hi:",["ifile="])
    except getopt.GetoptError:
        print('analyse.py -i <inputfile>')
        sys.exit(2)

    #compare(sys.argv[1], sys.argv[2])
    plot_similar()


