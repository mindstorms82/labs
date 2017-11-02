#!/usr/bin/python3

import sys, getopt
from conf import *
import pymysql.cursors
import re
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
            table = re.search('\w+', table).group(0)
            return table
    return False

def connect_db():
    cnx = pymysql.connect(host       = config['host'],
                             user    = config['user'],
                             password= config['password'],
                             db      = config['db'])
    cursor = cnx.cursor()
    return cursor, cnx

def create_tables():
    cursor, cnx = connect_db()
    #to create a table:
    for table in ['ebay', 'facebook', 'youtube', 'skype']:
        table = re.search('\w+', table).group(0)
        cursor.execute('CREATE TABLE IF NOT EXISTS `wireshark`.`%s`(`frame.number` int(4), `day` int(4), `year` int(4), `frame.time` varchar(30), `ip.src` varchar(15), `ip.dst` varchar(15), `tcp.port` int(5), `frame.len` int(4), `tcp.flags` varchar(10)) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci', (table))
        cnx.commit()


def sql(file_name):
    table_name = find_name(file_name)
    cursor, cnx = connect_db()

    with open(file_name, newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=' ', quotechar=',')
        next(csv_data)
        for row in csv_data:
            row[0] = row[0].replace(',Nov', '')
            del(row[1]) #remove
            row[1] = row[1].replace(',','')
            row[4] = row[4].replace('CET,', '')
            elements = row[4].split(",")
            i = 4
            for element in elements:
                row.insert(i, element)
                i = i + 1
            row = row[:-1] #remove last element
            print(row)
            row.insert(0, "table_name")
            cursor.execute("INSERT INTO `%s` (`frame.number`, `day`, `year`, `frame.time`, `ip.src`, `ip.dst`, `tcp.port`, `frame.len`, `tcp.flags`)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (row))
            cnx.commit()
    cnx.close()

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
   #create_tables()
   sql(argv)

if __name__ == "__main__":
    main(sys.argv[1])

