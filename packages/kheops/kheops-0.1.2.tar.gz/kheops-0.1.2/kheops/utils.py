# utils.py
import json
import pandas as pd
from tqdm import tqdm
import pkgutil

def load_data(file_name='data/mmlu.jsonl'):
    """Reads a JSONL file from the package and returns a DataFrame."""
    data = []
    
    # Load the file using pkgutil to ensure compatibility with package resources
    file_path = pkgutil.get_data(__name__, file_name)
    lines = file_path.decode('utf-8').splitlines()
    
    for line in lines:
        data.append(json.loads(line.strip()))
        
    return pd.DataFrame(data)

def InferenceEvalMMLU(df,srv, n_example=30):
    """Evaluates the LLM on MMLU dataset."""
    from kheops.core import call_llm
    score = 0
    ev_df = df.head(n_example)
    for index, row in tqdm(ev_df.iterrows(), total=len(ev_df), desc="Evaluation process"):
        result = call_llm(srv, row['topic'], row['question'], row['answer_a'], row['answer_b'], row['answer_c'], row['answer_d'])
        if str(result).strip().lower() == str(row['correct_answer']).strip().lower():
            score += 1
        print(f"Expected answer : {result}, ////   the correct answer : {row['correct_answer']}, /// the SCORE is : {score}")
    print(f"The score of evaluation with {n_example} examples is : {score/len(ev_df)}")
