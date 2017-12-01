#!/usr/bin/python3

import sys
import numpy as np
from sklearn.metrics import jaccard_similarity_score
from msql.py import connect_db
import matplotlib.pyplot as plt
import pymysql.cursors
from argparse import *

config = {
    'user': 'wire',
    'password': 'sjdoijwe9r0',
    'host': '192.168.1.101',
    'db': 'wireshark',
}



# Global lists #

# Main list #
model_names = (
    'facebook',
    'ebay',
    'skype1',
    'youtube'
 )

# lite is a modified version of model_names for more performance #
model_names_lite = (
    'facebook_lite',
    'ebay_lite',
    'skype1',
    'youtube_lite'
 )

# Debug List #
model_names_debug = (
    'skype_clone',
    'skype_clone',
    'skype_clone',
    'skype_clone'
)

lower_range = 0
upper_range = 100
# Small values are presented with better, the scale 1000 don't effect the comparing process
scale = 1000

def connect_db():
    cnx = pymysql.connect(host=config['host'],
                          user=config['user'],
                          password=config['password'],
                          db=config['db'])
    cursor = cnx.cursor()
    return cursor, cnx


def mysql_pred(cursor, cnx, table_name, lower_limit=lower_range, upper_limit=upper_range):
    print(lower_limit, upper_limit)
    result = []
    cursor.execute("SELECT `id`, `frame.len`, `tcp.flags` FROM `%s`", table_name)
    cnx.commit()
    for lene in cursor:
        if int(lower_limit) < lene[0] <= int(upper_limit):
            result.append(lene[1])
    return result
# END Function #


def mysql_true(cursor, cnx, table_name, lower_limit=0, upper_limit=0):
    result = []
    cursor.execute("SELECT `id`, `frame.len`, `tcp.flags` FROM `%s`", table_name)
    cnx.commit()
    for lene in cursor:
        if int(lower_limit) < lene[0] <= int(upper_limit):
            result.append(lene[1])
    return result
# END Function #


def average_value(cursor, cnx, table_name):
    result = []
    cursor.execute("SELECT `frame.number`, `frame.len`, `tcp.flags` FROM `%s`", table_name)
    cnx.commit()
    for lene in cursor:
        result.append(lene[1])
    average = sum(result) / len(result)
    return average
# END Function #


def maximum_value(cursor, cnx, table_name):
    result = []
    cursor.execute("SELECT `id`, `frame.len`, `tcp.flags` FROM `%s`", table_name)
    cnx.commit()
    for lene in cursor:
        result.append(lene[1])
    return max(result)
# END Function #


def get_maximum_input(cursor, cnx, table_name):
    cursor.execute("SELECT COUNT(*) FROM `%s`", table_name)
    cnx.commit()
    number_of_rows = cursor.fetchone()[0]
    return number_of_rows
# END Function #


def graph_bar(values, plot_name,lower_limit, upper_limit=0):
    x_pos = np.arange(len(model_names))
    fig, ax = plt.subplots(figsize=(3,11))
    ax.grid(True)
    ax.set_title('Web Applications Likelihood')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(model_names, rotation='horizontal')
    ax.set_ylabel(plot_name)
    ax.set_ylim((lower_limit * 0.1), (upper_limit + 100))
    # ax.set_ylim((lower_limit * 0.1), (100))
    ax.bar(x_pos, values, alpha=0.5, color=['b'])
    ax.minorticks_on()
    plt.tight_layout()
    plt.show()
# END Function #


def graph_pie(values, plot_name):

    _, ax = plt.subplots()
    ax.grid(True)
    ax.set_title(plot_name)
    shadow_triger = False if 0.0 in values else True
    patches, texts, autotexts = ax.pie(values, labels=model_names, autopct='%2.0f%%',
                                       shadow=shadow_triger, startangle=20, radius=1)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    # Resize the labels
    for t in texts:
        t.set_size('smaller')

    plt.show()
# END Function #


def mysql_static_true(cursor, cnx, table_name, val):
    cursor.execute("SELECT * FROM `%s` WHERE `frame.len` = %s", (table_name, val))
    cnx.commit()
    return cursor.rowcount


def statistic(cursor, cnx, table_name_true, value):
    maximum = get_maximum_input(cursor, cnx, table_name_true)
    packet_true = mysql_static_true(cursor, cnx, table_name_true, value)
    return (packet_true / maximum) * scale


def mysql_static_pred(cursor, cnx, table_name):
    result = []
    cursor.execute("SELECT `id`, `frame.len`, `tcp.flags` FROM `%s`", table_name)
    cnx.commit()
    arb = 10
    for lene in cursor:
        if id == arb & id <= 50:
            arb = arb + 10
            result.append(len[1])
    return result
# END Function #


def compare(table_name_true, table_name_pred, lower_limit_global, upper_limit_global, graphix=False):
    cursor, cnx = connect_db()
    average_values = []
    ticks = upper_limit_global - lower_limit_global
    upper_limit_internal = 0
    output_percentage = []

    if graphix:
        for table in model_names:
            average_values.append(round(average_value(cursor, cnx, table)))
        graph_bar(average_values, 'Packet_length', min(average_values), max(average_values))

    max = get_maximum_input(cursor, cnx, table_name_true)
    packet_pred = mysql_pred(cursor, cnx, table_name_pred, lower_limit_global, upper_limit_global)
    print(packet_pred)

    for lower_limit in range(1, max, ticks):
        upper_limit_internal = max if upper_limit_internal > max else lower_limit + ticks
        packet_true = mysql_true(cursor, cnx, table_name_true, lower_limit, upper_limit_internal)
        if len(packet_true) != len(packet_pred):
            packet_pred = packet_pred[0:len(packet_true)]
        output_percentage.append(jaccard_similarity_score(packet_true, packet_pred))

    tmp = outputo(output_percentage)
    tmp = tmp * 100
    print("Library name: ", table_name_true, "\n")
    return tmp
# END Function #


def outputo(ls):
    tmp = ls[:]
    return max(tmp)
# END Function #


def plot_similar(table_name_internal, lower_limit, upper_limit):
    values_internal = []
    for module_name in table_name_internal:
        values_internal.append(compare(module_name, 'alexa', lower_limit, upper_limit))

    print(values_internal)
    graph_bar(values_internal, 'Packet Similarity', min(values_internal), max(values_internal))
# END Function #


def plot_statistic(value=0, table_name_pred=None):
    cursor, cnx = connect_db()
    values_internal = []

    for table_name_true in model_names_lite:
            values_internal.append(statistic(cursor, cnx, table_name_true, value))

    if all(v == 0 for v in values_internal):
        print("No matches found! \n")
        return
    graph_pie(values_internal, 'Packet Likelihoods')
# End Function #


def usage():
    print("################################")
    print("Author: Alaa Alhamouri 2017")
    print("################################\n")
    print("This tool compares user packet "
          "length input with a MySQL database. "
          "It returns likelihoods between the applications Ebay, "
          "Facebook, Skype, Youtube and the user input"
          " ")
    print("\n\n")
    print("-s, --single expect \t enter a single packet length <= 5000")
    print("-r, --range \t enter a range of packet ids, for instance "
          "90 100, this means the tool will fetch 10 packet length"
          "from the database, fetch the packet length starting from "
          "the entry id 90 to 100\n")
    print(">>>>Use this tool on your own risk<<<<")
# End Function #


# MainFunction #
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', '--single', help="Enter a single packet length", type=int)
    parser.add_argument('-r', '--range', help="Enter a range of packet lengths, for instance 90 100", type=str)
    parser.add_argument('-v', '--verbose', help="This parameter is deactivated, only available for developers")
    parser.add_argument('-d', '--debug', action='store_true', help="Enter Debug mode for fast black box test")
    args = parser.parse_args()

    # Enter debug mode if -d is active else switch to normal mode
    table_name = model_names_debug if args.debug else model_names_lite
    if args.debug:
        print("####Debug mode is activated, small MySQL tables are used for tests, ignore the results####\n\n")

    if args.verbose:
        verbose = True
    elif args.single:
        plot_statistic(value=args.single)
    elif args.range:
        my_list = [int(item) for item in args.range.split(',')]
        lower_input = my_list[0] if my_list[0] < my_list[1] else my_list[1]
        upper_input = my_list[1] if my_list[0] < my_list[1] else my_list[0]
        plot_similar(table_name, lower_input, upper_input)
    else:
        print("unhandled option \n")
        sys.exit()

    # compare(sys.argv[1], sys.argv[2])
    # plot_similar()



