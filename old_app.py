from flask import Flask, redirect, url_for, request

import os



'''

import json
import pandas as pd
import geopandas as gpd

import psycopg2
import boto3
'''


'''

s3 = boto3.client('s3')
def lambda_handler(event, context):
    # TODO implement
    bucket = 'akshay-api-bucket'
    key = event['file_name']+'.csv'
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body']
    df_csv = pd.read_csv(content)
    component1 = event['component1']
    component2 = event['component2']
    component3 = event['component3']
    component1_df = df_csv[component1]
    component1_df["Component_E"] = 0
    for variable in component1:
        component1_df["Component_E"] = component1_df["Component_E"] + component1_df[variable]
    component1_df["Component_E"] = component1_df["Component_E"] / len(component1)
    component1_df["Component_E"] = (component1_df["Component_E"] - component1_df["Component_E"].min())/(component1_df["Component_E"].max() - component1_df["Component_E"].min())

	#Calculate Component S

    component2_df = df_csv[component2]
    component2_df["Component_S"] = 0
    for variable in component2:
        component2_df["Component_S"] = component2_df["Component_S"] + component2_df[variable]
    component2_df["Component_E"] = component2_df["Component_S"] / component2_df["Component_S"]
    component2_df["Component_S"] = (component2_df["Component_S"] - component2_df["Component_S"].min())/(component2_df["Component_S"].max() - component2_df["Component_S"].min())

	#Calculate Component AC

    component3_df = df_csv[component3]
    component3_df["Component_AC"] = 0
    for variable in component3:
        component3_df["Component_AC"] = component3_df["Component_AC"] + component3_df[variable]
    component3_df["Component_AC"] = (component3_df["Component_AC"] - component3_df["Component_AC"].min())/(component3_df["Component_AC"].max() - component3_df["Component_AC"].min())

	#Calculate Index

    df_csv["Component_E"] = component1_df["Component_E"]
    df_csv["Component_S"] = component2_df["Component_S"]
    df_csv["Component_AC"] = component3_df["Component_AC"]
    df_csv["Index"] = df_csv["Component_E"] + df_csv["Component_S"] - df_csv["Component_AC"]
    df_csv["Index"] = (df_csv["Index"] - df_csv["Index"].min())/(df_csv["Index"].max() - df_csv["Index"].min())


    return df_csv[["WKT", "GEOID", "Component_E", "Component_S", "Component_AC", "Index"]].to_json()


def select_city(event, context):
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


'''

app = Flask(__name__)


@app.route('/')
def index():
    return 'Urban Heat Resilient Vulnerability API' 

'''

@app.route('/select_continent')
def select_continent():
    
    event = {
        "cities": [
            "Brno",
            "Busan",
            "Frankfurt",
            "Riga",
            "Seoul",
            "Tokyo"
        ]
    }
    context = {}

    return select_city(event, context)
'''


if __name__ == '__main__':
    _debug = app.config.get('DEBUG', False)

    kwargs = {
        'host': os.getenv('FLASK_HOST', '0.0.0.0'),
        'port': int(os.getenv('FLASK_PORT', '5000')),
        'debug': _debug,
        'use_reloader': app.config.get('USE_RELOADER', _debug),
        **app.config.get('SERVER_OPTIONS', {})
    }

    app.run(debug=True)

    # app.run(**kwargs)