#!/usr/bin/python3

import sys, getopt
from conf import *
import pymysql.cursors

import csv

def read_csv(file_name):
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', quotechar=',')
        for row in csv_reader:
            elements = row[0].split(",")
            print(elements)

def find_name(file_name):
    for table in ["ebay","facebook","youtube","skype"]:
        if table in file_name:
            return table
    return False

def connect_db(fiel_name):
    cnx = pymysql.connect(host       = config['host'],
                             user    = config['user'],
                             password= config['password'],
                             db      = config['db'])
    cursor = cnx.cursor()
    return cursor

def create_table(file_name):
    cursor = connect_db(file_name)

    #to create a table:
    cursor.execute('CREATE TABLE IF NOT EXISTS `wireshark`.`%s` (`frame.number` int(4), `frame.time_relative` decimal(11,9), `ip.src` varchar(15), `ip.dst` varchar(15), `tcp.port` int(5), `frame.len` int(4), `tcp.flags` varchar(10)) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci', file_name)



def sql(file_name):
    table_name = find_name(file_name)
    cursor = connect_db(file_name)

    if not cursor.execute("SELECT * FROM `%s`, file_name"):
        create_table(file_name)

    with open(file_name, newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=' ', quotechar=',')
        for row in csv_data:
            elements = row[0].split(",") #frame.number,frame.time_relative,ip.src,ip.dst,tcp.port,frame.len,tcp.flags
            print()
            cursor.execute("INSERT INTO `wireshark`.`%s` (`frame.number`, `frame.time_relative`, `ip.src`, `ip.dst`, `tcp.port`, `frame.len`, `tcp.flags`)  VALUES('%s','%s','%s','%s','%s','%s','%s')", file_name, elements)
    cursor.close()

def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print('mysql.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('mysql.py -i <inputfile> -o')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = argv
   sql(argv)

if __name__ == "__main__":
    main(sys.argv[1])

