# core.py
import json
import pandas as pd
from langchain_community.llms.huggingface_text_gen_inference import HuggingFaceTextGenInference
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from tqdm import tqdm

def generate_response(prompt):
    srv = "https://p39enpjgcmgi2wfo.us-east4.gcp.endpoints.huggingface.cloud"
    llm = HuggingFaceTextGenInference(
        inference_server_url=srv,
        max_new_tokens=1800,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=0.09,
        repetition_penalty=1.03,
        streaming=True,
        do_sample=True,
    )

    response = llm(prompt, callbacks=[StreamingStdOutCallbackHandler()])
    return response

def call_llm(topic, question, answer_a, answer_b, answer_c, answer_d):
    user_prompt = f'''
    <|im_start|>system 
    You are an advanced assistant that processes multiple-choice questions (MCQs). For each question, you will be provided with four options labeled A, B, C, and D. Your task is to determine the correct answer and return only the letter corresponding to the correct choice. Do not provide any explanations or additional text, just the letter.
    <|im_end|>User
    Here is a question on the topic of {topic}.
    
    Question: {question}
    
    Which of the following answers is correct?
    
    A. {answer_a}
    B. {answer_b}
    C. {answer_c}
    D. {answer_d}
    
    State the letter corresponding to the correct answer.
    <|im_end|> 
    <|im_start|>assistant'''
    response = generate_response(user_prompt)
    print(response)
    return response
