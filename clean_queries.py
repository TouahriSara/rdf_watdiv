import re

def clean_sparql_queries(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Define the regex pattern to capture queries, removing the #EOQ# separators
    cleaned_content = re.sub(r'#EOQ#\s*', '', content)

    # Write the cleaned content into a new output file
    with open(output_file, 'w') as file:
        file.write(cleaned_content)

# Usage
input_file = '/home/adminlias/ddd/Downloads/rdf-exp-master/queries/workloads/watdiv-1b/string/workload_20k/all_sequential_F_C_S_L.q' 
output_file = '/home/adminlias/Desktop/PFE /cleaned_output.q'

clean_sparql_queries(input_file, output_file)
