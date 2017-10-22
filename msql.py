import mysql.connector

cnx = mysql.connector.connect(user='root', password='comeonin', host='127.0.0.1', database='boxresults')
cursor = cnx.cursor()
csv_data = pd.read_csv('Betting/boxresults3.csv')

for row in csv_data.iterrows():
    list = row[1].values
    cursor.execute("INSERT INTO table1(Week, Day, Date, Winner, Loser, PtsW, PtsL, YdsW, TOW, YdsL, TOL) VALUES('%d','%s','%s','%s','%s','%d','%d','%d','%d','%d', '%d')" % tuple(list))

cursor.close()
cnx.close()