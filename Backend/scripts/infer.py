# scripts/infer.py

import os
import torch
from transformers import LLaMATokenizer, LLaMAModel

MODEL_PATH = "models/trained_model"

def load_model():
    tokenizer = LLaMATokenizer.from_pretrained(MODEL_PATH)
    model = LLaMAModel.from_pretrained(MODEL_PATH)
    return tokenizer, model

def infer(build_sequence):
    tokenizer, model = load_model()
    inputs = tokenizer(build_sequence, return_tensors="pt")
    outputs = model(**inputs)
    return outputs

if __name__ == "__main__":
    build_sequence = "Initial items for Anti-Mage"
    output = infer(build_sequence)
    print(f"Inference result: {output}")
