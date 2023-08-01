import psycopg2
import psycopg2.extras
import csv

csv_file_path = "output.csv"

conn = psycopg2.connect(dbname='dbsample', user='postgres', password='ecotenistheway', host='test-data-1-instance-1.cteav6vpg16n.eu-central-1.rds.amazonaws.com', port='5432', sslmode='require')
nt_cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

try:
    # file=open("select_function.sql","r")
    file=open("1st_function.sql","r")
    # file=open("2nd_function.sql","r")

    sql1=file.read()
    # print(sql)

    nt_cur = conn.cursor()
    nt_cur.execute(sql)
    results = nt_cur.fetchall()
    
    print("result: ")
    print(results)

    nt_cur.close()

    with open(csv_file_path, 'w', newline='') as csvfile:
        headerlist = ['customer_id', 'customer_name', 'product_name']
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', dialect='excel',quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(headerlist)
        
        for row in results:
            csvwriter.writerow(row)

except (Exception, psycopg2.DatabaseError) as error:
    print("no success: ")
    print(error)

finally:
    if  nt_cur is not None:
        nt_cur.close()

