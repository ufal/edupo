import argparse
import os
import json
import re
import random

from openai import OpenAI
client = OpenAI()

from tqdm import tqdm

from poet_utils import StropheParams

#from llama_cpp import Llama

parser = argparse.ArgumentParser()

parser.add_argument("--data_path",  default=os.path.abspath(os.path.join(os.path.dirname(__file__),'..', "corpusCzechVerse", "ccv")), type=str, help="Path to Data")
parser.add_argument("--result_data_path",  default=os.path.abspath(os.path.join(os.path.dirname(__file__),'..', "corpusCzechVerse", "ccv-new-summary")), type=str, help="Path to Data")

if __name__ == '__main__':
    args = parser.parse_args([] if "__file__" not in globals() else None)

os.makedirs(args.result_data_path, exist_ok=True)

dataset= os.listdir(args.data_path)
random.shuffle(dataset)

dataset = dataset[:11]

for poem_file in tqdm(dataset):
    if not os.path.isfile(os.path.join(args.data_path, poem_file)) or os.path.exists(os.path.join(args.result_data_path, poem_file)):
        continue

    file = json.load(open(os.path.join(args.data_path, poem_file) , 'r'))
        
    for i, poem_data in enumerate(file):
        try:
            poem_text = [] 
            autor = 'Unknown' 
            if poem_data['biblio']['p_title'] != None:
                poem_text.append(poem_data['biblio']['p_title'])
            else:
                poem_text.append("NO TITLE")
                
            if  "p_author" in poem_data.keys() and 'identity' in poem_data['p_author'].keys():
                autor = poem_data['p_author']['identity']
            for strophe in poem_data['body']:
                    for verse in strophe:
                        poem_text.append(verse['text'])
                    poem_text.append("\n")
            poem = "\n".join(poem_text)
            input_text = f"Categories: {', '.join(StropheParams.POEM_TYPES)}. Author: {autor}\nPoem:\n{poem}\nBest Category:"

            system = "You are an assistent that is proficient in poem categorization."

            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": input_text}
                ]
            )
            categories = completion.choices[0].message.content
        
            #categories = list(map(str.strip, re.findall(r'\w+', categories)))
            #categories = list(filter(lambda x: len(x) > 0, categories))
            #categories = list(filter(lambda x: x in StropheParams.POEM_TYPES, categories))

            file[i]['categories'] = categories
        
            input_text = f"Author: {autor}\nPoem:\n{poem}\nPoem summarization: "
            
            system = "You are a assistent that is proficient in poem summarization."

            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": input_text}
                ]
            )
            sumarization =  completion.choices[0].message.content

            file[i]['sumarization'] = sumarization
            
            input_text = f"Author: {autor}\nPoem:\n{poem}\nPoem summarization in Czech: "
            
            system = "You are a Czech assistent that is proficient in poem summarization."

            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": input_text}
                ]
            )
            cs_sumarization =  completion.choices[0].message.content

            file[i]['cs_sumarization'] = cs_sumarization
        
        except Exception as e:  
            print("Context too large: ", repr(e))
        
    json.dump(file, open(os.path.join(args.result_data_path, poem_file), 'w+'), indent=6)   
