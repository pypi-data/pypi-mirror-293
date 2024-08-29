import argparse
import json
import gzip
import os

from tqdm import tqdm

def convert_text_format_in_folder(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    for file_name in tqdm(os.listdir(input_folder_path)):
        if file_name.endswith('.jsonl.gz'):
            input_file_path = os.path.join(input_folder_path, file_name)
            output_file_path = os.path.join(output_folder_path, file_name)
            
            with gzip.open(input_file_path, 'rt', encoding='utf-8') as file:
                lines = file.readlines()
            
            formatted_data = []
            for line in lines:
                data = json.loads(line)
                text_entries = data['text']
                formatted_entry = []
                for entry in text_entries:
                    role = entry['role'].upper()
                    content = entry['content']
                    formatted_entry.append(f"{role}: {content}")
                data['text'] = "\n\n".join(formatted_entry)
                formatted_data.append(data)
            
            with gzip.open(output_file_path, 'wt', encoding='utf-8') as outfile:
                for entry in formatted_data:
                    json.dump(entry, outfile)
                    outfile.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Save huggingface dataset to jsonl.gz files"
    )
    parser.add_argument("--in_path", type=str, required=True)
    parser.add_argument("--out_path", type=str, required=True)
    args = parser.parse_args()

    input_folder_path = args.in_path
    output_folder_path = args.out_path
    
    convert_text_format_in_folder(input_folder_path, output_folder_path)
