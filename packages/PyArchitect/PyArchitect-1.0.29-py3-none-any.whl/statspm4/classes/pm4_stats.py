import logging
import os
import csv
import pandas as pd # type: ignore

logger = logging.getLogger("pyarchitect")

class Pm4Stats:
    
    def init(self):
        pass
    
    
    def read_csv_with_single_header(file_path):
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            # Read the first row and trim spaces from the column titles
            header = next(reader)
            header = [col.lower().replace('"', '').replace("'", '').strip() for col in header]
            
            # Initialize a list to store the rows
            rows = []
            
            for row in reader:
                # Skip rows that match the header
                if [col.lower().replace('"', '').replace("'", '').strip() for col in row] == header:
                    continue
                
                new_row = {}
                for index, key in enumerate( header):
                    new_row[key] = row[index].replace('"', '').replace("'", '').strip()
                rows.append(new_row)
            
            return header, rows

    def cloneTo100k(new_row, pr_row_qt):
        # Calculate the proportional increment factor
        increment_factor = pr_row_qt / new_row['pr_rows']
        increment_prt_factor = increment_factor

        # Clone the new_row and modify it
        cloned_row = new_row.copy()

        # Update pr_rows to 100000
        cloned_row['pr_rows'] = pr_row_qt

        # Update pr_deleted_rows and pr_data_mb proportionally
        cloned_row['pr_deleted_rows'] = int(cloned_row['pr_deleted_rows'] * increment_factor)
        cloned_row['pr_data'] = int(cloned_row['pr_data'] * increment_factor)

        # Recalculate dependent fields
        cloned_row['pr_avg_row'] = cloned_row['pr_avg_row'] 

        # Recalculate PRT dependent fields
        cloned_row['prt_rows'] = int(cloned_row['prt_rows'] * increment_prt_factor)
        cloned_row['prt_deleted_rows'] = int(cloned_row['prt_deleted_rows'] * increment_prt_factor)
        cloned_row['prt_data'] = int(cloned_row['prt_data'] * increment_prt_factor)
        
        cloned_row['total_data'] = int(cloned_row['pr_data'] + cloned_row['prt_data'])
        cloned_row['total_avg_case_length'] = int((cloned_row['pr_data'] + cloned_row['prt_data']) / cloned_row['pr_rows'])

        # Append the cloned and modified row to the result list
        return cloned_row
            
        
    def process(csv_path: str):

        data = []

        # Iterate over all files in the input folder
        for filename in os.listdir(csv_path):
            # Check if the file has a .csv extension
            if filename.endswith('.csv'):
                logger.debug(filename)
                csv_file = os.path.join(csv_path, filename)
                header, rows = Pm4Stats.read_csv_with_single_header(csv_file)

                # Append the rows to the data list
                data.extend(rows)
                
        # Create DataFrame
        df = pd.DataFrame(data)
        #print(df.columns)
        
        #unique_schemas = df['table_schema'].unique()
        #for schema in unique_schemas:
        #    print(schema)
        
        # Group by schema
        grouped = df.groupby('table_schema')


        # Access the group where table_schema is 'pm4_intembeko'
        pm4_intembeko_group = grouped.get_group('pm4_intembeko')

        # Print the group
        #print(pm4_intembeko_group)

        # Initialize the result list
        result = []

        # Iterate over each group
        for schema, group in grouped:
            # Check if both tables are present
            if set(group['table_name']) >= {'process_requests', 'process_request_tokens'}:
                # Extract data for process_requests
                pr = group[group['table_name'] == 'process_requests'].iloc[0]
                # Extract data for process_request_tokens
                prt = group[group['table_name'] == 'process_request_tokens'].iloc[0]
                
                auto_increment_pr = 0 if pr['auto_increment'] == 'NULL' else int(pr['auto_increment'])
                auto_increment_prt = 0 if prt['auto_increment'] == 'NULL' else int(prt['auto_increment'])
                
                
                pr_rows =  int(pr['table_rows'])
                prt_rows = int(prt['table_rows'])
                
                pr_data  = int(pr ['data_length'])                 
                prt_data = int(prt['data_length'])                 
                # Create the new structure
                new_row = {
                    'schema': schema,
                    'pr_auto_incr': auto_increment_pr,
                    'pr_rows': pr_rows,
                    'pr_deleted_rows': auto_increment_pr - pr_rows,
                    'pr_avg_row': int(pr_data / pr_rows),
                    'pr_data': int(pr_data),
                    'prt_auto_incr': auto_increment_prt,
                    'prt_rows': prt_rows,
                    'prt_deleted_rows': auto_increment_prt - prt_rows,
                    'prt_avg_row': int(prt_data / prt_rows),
                    'prt_data': int(prt_data),
                    
                    'total_data': int(pr_data + prt_data),
                    'total_avg_case_length': int( (pr_data + prt_data)/ pr_rows )
                }
                
                # Append to result list
                result.append(new_row)
                if pr_rows < 100_000:
                    result.append( Pm4Stats.cloneTo100k(new_row, pr_rows * 2))
                
                if  pr_rows > 100_000 and pr_rows < 500_000:
                    result.append( Pm4Stats.cloneTo100k(new_row, pr_rows * 1.5))
                
                if  pr_rows > 500_000 and pr_rows < 1_000_000:
                    result.append( Pm4Stats.cloneTo100k(new_row, pr_rows * 1.2))

        # Convert result to DataFrame for better visualization
        result_df = pd.DataFrame(result) 

        # Sort the DataFrame by the 'pr_rows' column
        #sorted_df = result_df.sort_values(by='pr_rows', ascending=False)

        # Display the result
        #print(sorted_df)
        
        #sorted_df2 = result_df.sort_values(by='pr_avg_row', ascending=False)
        #print(sorted_df2)
        
        sorted_df3 = result_df.sort_values(by='schema', ascending=True)
        print(sorted_df3)   
        
        # Export to CSV
        sorted_df3.to_csv('output.csv', index=False)
             
