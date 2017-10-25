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
def sql(file_name):
    cnx = pymysql.connect(host       = config['host'],
                             user    = config['user'],
                             password= config['password'],
                             db      = config['db'])
    cursor = cnx.cursor()
    table_name = find_name(file_name)
    with open(file_name, newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=' ', quotechar=',')
        for row in csv_data:
            elements = row[0].split(",") #frame.number,frame.time_relative,ip.src,ip.dst,tcp.port,frame.len,tcp.flags
            cursor.execute("INSERT INTO table_name(frame.number,frame.time_relative,ip.src,ip.dst,tcp.port,frame.len,tcp.flags) VALUES('%d','%f','%s','%s','%d','%d','%s')", elements)
    cursor.close()
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
   read_csv(argv)

if __name__ == "__main__":
    main(sys.argv[1])

