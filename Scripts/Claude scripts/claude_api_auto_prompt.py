import anthropic
import json
from typing import List, Dict
import time

"""
Usage Instructions
------------------

This script queries Claude (Claude-Sonnet-4.5) with a set of multiple-choice
clinical vignettes (these can be found in the github in the datsets folder) and saves the model's reasoning, answer choice, and
confidence for each case in a JSON.

The script expects a JSON file containing clinical vignettes in the format:
    [
        {
            "case_id": "CV_001",
            "question": "A patient presents with...",
            "options": {"A": "...", "B": "...", ...},
            "answer": "B",
            "answer_idx": 1
        },
        ...
    ]

To run script:
python run_claude_vignette_eval.py

Output:
Results will be saved as a JSON list containing:
    - case_id
    - original question and options
    - correct answer
    - full Claude response (reasoning, answer, confidence)

This script is part of the ECS 289G project evaluating LLM diagnostic reasoning and was made with assistance of LLMs.
"""

def load_clinical_vignettes(filepath: str) -> List[Dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_question_with_options(vignette: Dict) -> str:
    question = vignette['question']
    options = vignette['options']
    
    # Format options as A, B, C, D, E
    formatted_options = "\nOptions:\n"
    for key in sorted(options.keys()):
        formatted_options += f"{key}. {options[key]}\n"
    
    return f'"{question}{formatted_options}"'

def call_claude_api(client: anthropic.Anthropic, question_text: str) -> str:
    """Make API call to Claude."""
    system_prompt = """You are a medical reasoning assistant. Answer the following multiple-choice clinical question below by selecting the single best answer (A, B, C, D, etc.). 
First, provide a short explanation of your clinical reasoning (3–6 sentences). 
Then select the single best answer choice.
Then provide your confidence (0–100%).
Format:
Reasoning: <your step-by-step explanation>
Answer: <letter>
Confidence: <0–100%>
Do not introduce clinical details not present in the question.
Question:"""
    
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=20000,
        temperature=1,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question_text
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def process_vignettes(input_filepath: str, output_filepath: str, api_key: str): 
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"Loading vignettes from {input_filepath}...")
    vignettes = load_clinical_vignettes(input_filepath)
    print(f"Loaded {len(vignettes)} vignettes")
    
    # Process each vignette
    results = []
    for idx, vignette in enumerate(vignettes, 1):
        print(f"\nProcessing vignette {idx}/{len(vignettes)} (Case ID: {vignette['case_id']})")
        
        try:
            question_text = format_question_with_options(vignette)
            response = call_claude_api(client, question_text)
            
            # Create result entry matching GPT-4 format
            result = {
                "case_id": vignette['case_id'],
                "original_question": vignette['question'],
                "original_options": vignette['options'],
                "original_answer": vignette['answer'],
                "original_answer_idx": vignette['answer_idx'],
                "claude_response": response
            }
            
            results.append(result)
            print(f"✓ Successfully processed {vignette['case_id']}")
            
            # small delay added here to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"✗ Error processing {vignette['case_id']}: {str(e)}")
            # Continue with next vignette even if one fails
            continue
    
    # Save results
    print(f"\n\nSaving results to {output_filepath}...")
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully saved {len(results)} results")


if __name__ == "__main__":
    # Configuration
    INPUT_FILE = "clinical_vignettes_dataset.json"
    OUTPUT_FILE = "claude_responses_clinical_vignettes_Chain-of-thought.json"
    API_KEY = "XXX"  # rember to replace with the API key you will use

    process_vignettes(INPUT_FILE, OUTPUT_FILE, API_KEY)