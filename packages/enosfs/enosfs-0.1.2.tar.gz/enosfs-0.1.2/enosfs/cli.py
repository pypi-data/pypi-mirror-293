#!/usr/bin/env python3

import pandas as pd
import argparse
from google.cloud import bigtable

def ingest(csv_fp,project_id,instance_id,table_id,column_family,row_key_column):

    df = pd.read_csv(csv_fp)

    client = bigtable.Client(project=project_id,admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    for index, row_data in df.iterrows():
        row_key = str(row_data[row_key_column])
        bigtable_row = table.direct_row(row_key)

        for column in df.columns:
            if column!= row_key_column:
                bigtable_row.set_cell(column_family,column,str(row_data[column]))
        
        bigtable_row.commit()
    
    print('Data inserted successfully')

def main():
    valid_project_ids = ['rsg-enos-private-dev',
                         'rsg-enos-private-shared',
                         'rsg-enos-private-prod',
                         'rsg-enos-dev',
                         'rsg-enos-shared',
                         'rsg-enos-prod'
                         ]
    parser = argparse.ArgumentParser(description='Ingest Data into Enos Online Store (Bigtable)')
    parser.add_argument('--csv_fp', help='file path to CSV file')
    parser.add_argument('--project_id', help='GCP Project ID',choices=valid_project_ids)
    parser.add_argument('--instance_id', help='Bigtable Instance ID',default='enos-online-fs')
    parser.add_argument('--table_id', help='Bigtable Table ID ')
    parser.add_argument('--column_family', help='Column Family')
    parser.add_argument('--row_key_column', help='Row Key Column Name')

    args = parser.parse_args()
    
    ingest(csv_fp=args.csv_fp,
           project_id=args.project_id,
           instance_id=args.instance_id,
           table_id=args.table_id,
           column_family=args.column_family,
           row_key_column=args.row_key_column
        ) 
if __name__=='__main__':
    main()



