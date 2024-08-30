# resources/azgov.sql

import json
import os
import re
import sys
from pathlib import Path

import openai
import regex

# Get the directory containing the schema_analyzer package
package_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
# Add this directory to sys.path
sys.path.insert(0, package_dir)

from schema_analyzer.services.files import Files

def get_ai_analysis(prompt):
    output_file.write(f"### Analisys:\n\n")
    ai_answer = get_gpt_answer(prompt)
    output_file.write(f"{ai_answer}\n\n")    
    ai_file.write(f"{ai_answer}\n\n")    
    
    
def get_gpt_answer(prompt):
    # Make sure you add your API key
    openai.api_key = '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'
  
    system_prompt = Files.get_prompt('system')
    user_prompt = Files.get_prompt('analyze_db_sql')
    print (system_prompt)
    
    response = openai.chat.completions.create(
        model='gpt-4o',
        messages= [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},            
            {"role": "user",   "content": prompt},
    #        {"role": "assistant",   "content": ""},
        ],
        max_tokens = 4000,
        temperature = 0.0,
    )

    if not (hasattr(response, 'choices') and isinstance(response.choices, list)) and hasattr(response, 'usage') and hasattr(response, 'model'):
        raise AttributeError("OpenAI error in response")

    choice = response.choices[0]
    text = choice.message.content.strip()
    return text 


def extract_plantuml_content(plantuml_content):
    pattern = r'```plantuml(.*?)```'
    result = re.search(pattern, plantuml_content, re.DOTALL)
    if result:
        return result.group(1).strip()
    else:
        return None
    

def extract_json(json_content):
    pattern = r'```json(.*?)```'
    result = re.search(pattern, json_content, re.DOTALL)
    json_str = result.group(1).strip()
    if result:
        data = json.loads(json_str)
        return data
    else:
        return None
    

def save_plantuml(output_schema, answer):
    data = extract_json(answer)
    
    with open(output_schema, "w") as file: 
        file.write( """@startuml

left to right direction
skinparam roundcorner 8
skinparam shadowing true
skinparam handwritten false
skinparam linetype polyline

hide stereotypes 
hide methods
hide circle

!define table(x) entity x << (T, white) >>
""")
        for table in data['tables']:
            file.write(f"  table({table}) {{}} \n")
        file.write(f"\n")

        for relationship in data['relationships']:
            file.write(f"  {relationship[0]} --> {relationship[1]} \n")
        file.write(f"\n")

        file.write("@enduml")

    print (f"{len(data['tables'])} tables")
    print (f"{len(data['relationships'])} relationships")
    return 

def main():
    print ("Schema Analyzer")

    schema_sql_path = os.path.join(Files.get_root_path(), 'resources', 'azgov.sql')
    #schema_sql_path = os.path.join(Files.get_root_path(), 'resources', 'demo.sql')
    output_schema = "/home/fernando/ProcessMaker/repos/pm4_diagrams/architecture/azgov/schema_level1.puml"

    with open(schema_sql_path, 'r') as file:
        # read file contents
        data = file.read()
        print ( len(data))

        answer = get_gpt_answer(data)
        save_plantuml(output_schema, answer)
            
main()    
exit (1)     
    
# specify the path here
path = '/home/fernando/ProcessMaker/repos/processmaker/database/migrations'
output_file_path = "output.md"
ai_file_path = "ai.md"

output_file = open(output_file_path, "w")
ai_file = open(ai_file_path, "w")

# create a sorted list of the files
filenames = sorted([f for f in os.listdir(path) if f.endswith(".php")])

file_index = 0
php_file_index = 0
# iterate over files in the specified directory

chunk_code = ""

for filename in filenames:
    php_file_index += 1
    if not php_file_index in range(30, 35):
        continue
    
    with open(os.path.join(path, filename), 'r') as file:
        # read file contents
        data = file.read()

        up_contents = ''
        
        # use regex to find the 'up' function contents
        up_function_pattern = r"public function up\(\)\s*({((?>[^{}]+|(?1))*)})"
        match = regex.search(up_function_pattern, data, regex.DOTALL | regex.MULTILINE)
        if match:
            up_contents = match.group(2) # Change to group(2)

        if not match:
            up_function_pattern = r"public function up\(\): void\s*{(.*?)}.*public function down"
            match = regex.search(up_function_pattern, data, regex.DOTALL | regex.MULTILINE)
            if match:
                up_contents = match.group(1) # Change to group(2)
            else:
                print (f" {filename} ") 

            
        if match:
            file_index += 1 

            # write file name and contents to output file
            output_file.write(f"## file: {file_index}: {filename}\n")
            output_file.write(f"```{up_contents}\n```\n\n")   

            chunk_code += up_contents
            if file_index % 2 == 0: 
                print (file_index)
                get_ai_analysis( chunk_code )
                chunk_code = ""
            
        else: 
            pass
            #print (f"{filename} ") 

if chunk_code != "": 
    get_ai_analysis( chunk_code )
    chunk_code = ""
    
print (f"{ file_index} of {php_file_index} files processed")    

# close the output file
output_file.close()
ai_file.close()

#title_counts, title_descriptions = count_title_occurrences(ai_file_path)
#
#print("Title Counts:")
#for title, count in title_counts.items():
#    print(f"{title}: {count}")
#    
    