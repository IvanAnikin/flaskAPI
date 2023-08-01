import json
import psycopg2

def lambda_handler(event, context):
    #Cities = ['Brno', 'Busan', 'Frankfurt', 'Riga', 'Seoul', 'Tokyo']
    Cities = event['cities']
    conn = psycopg2.connect(
    host="test-data-1-instance-1.cteav6vpg16n.eu-central-1.rds.amazonaws.com",
    database="dbsample",
    user="postgres",
    password="ecotenistheway")

    conn.autocommit = True
    cursor = conn.cursor()

    sql = "CREATE TEMPORARY TABLE TempStudents AS "
    sql +="SELECT * FROM database2 WHERE "
    for n in range (0, len(Cities)):
        if n == 0:
            sql = sql + "city ='" + Cities[n] + "'"
        if n > 0:
            sql = sql + "OR city ='" + Cities[n] + "'"
    sql = sql + ";"
    sql += "ALTER TABLE TempStudents DROP COLUMN geom;"
    sql += "SELECT * FROM TempStudents;"
    
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    result = []
    for row in rows:
        row = dict(zip(columns, row))
        result.append(row)
    
    json_object = json.dumps(result, indent=4, default=str)
    
    conn.commit()
    conn.close()    # TODO implement
    return {
        'statusCode': 200,
        'body': json_object
    }
