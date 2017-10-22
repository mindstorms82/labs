#!/usr/bin/python3

import sys, getopt

import pymysql.cursors

import csv

def read_csv(file_name):
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='', quotechar=',')
    print(csv_reader)
    return csv_reader

def sql(file_name):
    config = {
        'user': '',
        'password': '',
        'host': '',
        'database': '',
    }
    cnx = pymysql.connect(host='',
                             user='',
                             password='',
                             db='wireshark',)
    cursor = cnx.cursor()
    csv_data = read_csv(file_name)
    for row in csv_data.iterrows():
        list = row[1].values
        cursor.execute("INSERT INTO table1(frame.number,frame.time,ip.src,ip.dst,tcp.port,frame.len) VALUES('%d','%s','%s','%s','%s','%s','%s')" % tuple(list))
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
         inputfile = arg
   sql(inputfile)

if __name__ == "__main__":
    print("goroo")
    main(sys.argv[1:])

