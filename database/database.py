import psycopg2
import psycopg2.extras


def get_countries(continents):

    conn = psycopg2.connect(dbname='dbsample', user='postgres', password='ecotenistheway', host='test-data-1-instance-1.cteav6vpg16n.eu-central-1.rds.amazonaws.com', port='5432', sslmode='require')
    nt_cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    try:
        file1=open("database/1st_function_1.sql","r")
        sql1=file1.read()
        file2=open("database/1st_function_2.sql","r")
        sql2=file2.read()

        sql = sql1 + continents + sql2

        nt_cur = conn.cursor()
        nt_cur.execute(sql)
        results = nt_cur.fetchall()

        print("result: ")
        print(results)

        nt_cur.close()

        return results

    except (Exception, psycopg2.DatabaseError) as error:
        print("no success: ")
        print(error)

    finally:
        if  nt_cur is not None:
            nt_cur.close()
    
