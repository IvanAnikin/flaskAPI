import json
import pandas as pd
import boto3
import geopandas as gpd

s3 = boto3.client('s3')
#i have made a change
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

    #return df_csv.to_json()
    #return {
    #    'statusCode': 200,
    #    'body': json.dumps('Hello from Lambda!'+ str(df_csv.shape))
    #}
