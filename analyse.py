#!/usr/bin/python3

import sys
import numpy as np
from sklearn.metrics import jaccard_similarity_score
import matplotlib.pyplot as plt
import pymysql.cursors
from argparse import *
import plotly as pys

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

config = {
    'user': '',
    'password': '',
    'host': '',
    'db': '',
}

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
# END Function #


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


def graph_pie(values, plot_name, port_plot=0):

    _, ax = plt.subplots()
    ax.grid(True)
    plot_name = plot_name + " in port " + str(port_plot) if port_plot > 0 else plot_name
    ax.set_title(plot_name)
    shadow_triger = False if 0.0 in values else True
    for value in values:
        print(value)

    patches, texts, autotexts = ax.pie(values, labels=model_names, autopct='%2.0f%%',
                                       shadow=shadow_triger, startangle=20, radius=1)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    # Resize the labels
    for t in texts:
        t.set_size('smaller')

    plt.show()
# END Function #


def graph_pie_advanced(values_443, values_80, plot_name, value):
    fig = {
        "data": [
            {
                "values": values_443,
                "labels": model_names,
                "marker": {"colors": ['rgb(102,102,205)',
                                      'rgb(255,128,0)',
                                      'rgb(0,153,76)',
                                      'rgb(204,0,0)']},
                "domain": {"x": [0, .48]},
                "name": "Port 443",
                "textfont": {"color": ["#bebada", "#bebada", "#bebada", "#bebada"], "size": [22, 25, 26, 27]},
                "hoverinfo": "label+percent+name",
                "hole": .5,
                "type": "pie"
            },
            {
                "values": values_80,
                "labels": model_names,
                "marker": {"colors": ['rgb(102,102,205)',
                                      'rgb(255,128,0)',
                                      'rgb(0,153,76)',
                                      'rgb(204,0,0)']},
                "text": "Port 80",
                "textposition": "inside",
                "domain": {"x": [.54, 1]},
                "name": "Port 80",
                "hoverinfo": "label+percent+name",
                "hole": .5,
                "type": "pie"
            }],
        "layout": {
            "title": plot_name,
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Port 443",
                    "x": 0.20,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Port 80",
                    "x": 0.8,
                    "y": 0.5
                }
            ]
        }
    }
    #py.plot(fig, filename='donut')
    local_name = str(value) + "limited.html"
    pys.offline.plot(fig, filename=local_name)
# END Function #


def mysql_static_true(cursor, cnx, table_name, val, port_mysql=0, flag=None):
    if port_mysql == 0:
        cursor.execute("SELECT * FROM `%s` WHERE `frame.len` = %s AND `id` <= 30023", (table_name, val))
    else:
        if flag:
            cursor.execute("SELECT * FROM `%s` WHERE `frame.len` = %s AND `tcp.port` = %s AND `tcp.flags` = %s AND`id` <= 30023",
                           (table_name, val, port_mysql, flag))
        else:
            cursor.execute("SELECT * FROM `%s` WHERE `frame.len` = %s AND `tcp.port` = %s AND`id` <= 30023",
                           (table_name, val, port_mysql))
    cnx.commit()
    return cursor.rowcount
# END Function


def statistic(cursor, cnx, table_name_true, value, port_statistic=0, flag=None):
    maximum = get_maximum_input(cursor, cnx, table_name_true)
    packet_true = mysql_static_true(cursor, cnx, table_name_true, value, port_statistic, flag)
    result = (packet_true / maximum)
    return result * scale
# END Function #

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


def plot_statistic(value=0, port_plot=0, advance=False, flag=None):
    cursor, cnx = connect_db()
    values_internal = []
    values_443 = []
    values_80 = []
    if advance:
        for table_name_true in model_names:
                values_443.append(statistic(cursor, cnx, table_name_true, value, 443, flag))
        for table_name_true in model_names:
                values_80.append(statistic(cursor, cnx, table_name_true, value, 80, flag))

        if all(v == 0 for v in values_443) and all(v == 0 for v in values_80):
            print("No matches found! \n")
            return
        title = 'Packet likelihoods for ' + str(value) + ' Bytes'
        graph_pie_advanced(values_443, values_80, title, value)


    else:
        for table_name_true in model_names_lite:
                values_internal.append(statistic(cursor, cnx, table_name_true, value, port_plot))
        if all(v == 0 for v in values_internal):
            print("No matches found! \n")
            return
        title = 'Packet likelihoods for ' + str(value) + ' Bytes'
        graph_pie(values_internal, title, port_plot)
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

    print("-p, --port \t enter port number 443 or 80 are only available in this tool\n")

    print("-r, --range \t enter a range of packet ids, for instance "
          "90,100. This means the tool will fetch 10 packet length"
          "from the database, fetch the packet length starting from "
          "the entry id 90 to 100\n")

    print("-d, --debug \t enter the debug mode will activate a lite "
          "weight table for making quick test and response\n")

    print(">>>>Use this tool on your own risk<<<<")
# End Function #


# MainFunction #
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', '--single',  help="Enter a single packet length", type=int)
    parser.add_argument('-f', '--flag',  help="Enter a flag in Hex format", type=str)
    parser.add_argument('-p', '--port',    help="Enter port number in search", type=int)
    parser.add_argument('-a', '--advance', action='store_true', help="Adding this option will display separated charts")
    parser.add_argument('-r', '--range',   help="Enter a range of packet lengths, for instance 90 100", type=str)
    parser.add_argument('-v', '--verbose', help="This parameter is deactivated, only available for developers")
    parser.add_argument('-d', '--debug',   action='store_true', help="Enter Debug mode for fast black box test")
    parser.add_argument('-i', '--information', action='store_true', help="Print more information about the tool")
    args = parser.parse_args()

    # Enter debug mode if -d is active else switch to normal mode
    table_name = model_names_debug if args.debug else model_names_lite
    if args.debug:
        print("####Debug mode is activated, small MySQL tables are used for tests, ignore the results####\n\n")

    if args.verbose:
        verbose = True
    elif args.single:
        port_args = args.port if args.port else 0
        advance = True if args.advance else False
        plot_statistic(value=args.single, port_plot=port_args, advance=advance, flag=args.flag)
    elif args.range:
        my_list = [int(item) for item in args.range.split(',')]
        lower_input = my_list[0] if my_list[0] < my_list[1] else my_list[1]
        upper_input = my_list[1] if my_list[0] < my_list[1] else my_list[0]
        plot_similar(table_name, lower_input, upper_input)
    elif args.information:
        usage()
        sys.exit()
    else:
        print("Unhandled option \n")
        sys.exit()
