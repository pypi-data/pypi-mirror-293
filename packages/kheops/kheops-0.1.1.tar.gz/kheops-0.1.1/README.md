# Import functions from your package
from your_package_name import load_data, eval_mmlu

# Use the load_data function to load your dataset
file_path = 'mmlu.jsonl'  # Replace with the path to your JSONL file
df = load_data(file_path)

# Evaluate your LLM using the eval_mmlu function
eval_mmlu(df)
