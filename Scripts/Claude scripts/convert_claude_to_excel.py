import json
import pandas as pd
import re
from pathlib import Path

"""
Usage Instructions
------------------
This script takes the generated JSON file from the 'claude_auto_api_self_eval.py' script and parses it then added it to an Excel file
This script is part of the ECS 289G project evaluating LLM diagnostic reasoning and was made with assistance of LLMs.
"""

def parse_self_evaluation(self_eval_text):
    # parses the self-evaluation text to extract the individual scores from the resposnse
    scores = {
        'plausibility': '',
        'faithfulness': '',
        'calibration': '',
        'harmfulness': ''
    }
    
    if not self_eval_text:
        return scores
    
    plaus_match = re.search(r'Plausibility:\s*([\d.]+)', self_eval_text, re.IGNORECASE)
    if plaus_match:
        scores['plausibility'] = plaus_match.group(1)

    faith_match = re.search(r'Faithfulness:\s*([\d.]+)', self_eval_text, re.IGNORECASE)
    if faith_match:
        scores['faithfulness'] = faith_match.group(1)
    
    calib_match = re.search(r'Calibration:\s*([\d.]+)', self_eval_text, re.IGNORECASE)
    if calib_match:
        scores['calibration'] = calib_match.group(1)
    
    harm_match = re.search(r'(?:Harmfulness|Safety):\s*([\d.]+)', self_eval_text, re.IGNORECASE)
    if harm_match:
        scores['harmfulness'] = harm_match.group(1)

    return scores

def convert_json_to_excel(json_file_path, output_excel_path=None):
    """
    Convert JSON clinical vignette data to Excel format matching the provided template.
    
    Args:
        json_file_path: Path to the input JSON file
        output_excel_path: Path for the output Excel file (optional)
    """
    # reads in the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Prepare data for DataFrame
    rows = []
    
    for item in data:
        case_id = item.get('case_id', '')
        vignette = item.get('original_question', '')
        correct_diagnosis = item.get('original_answer', '')
        correct_answer_letter = item.get('original_answer_idx', '')
        
        # this gets Claude's response details
        claude_response = item.get('claude_initial_response', '')
        claude_answer = item.get('claude_answer_letter', '')
        claude_confidence = item.get('claude_confidence', '')
        claude_correct = item.get('claude_correct', False)
        
        # Parse self-evaluation
        self_eval_text = item.get('claude_self_evaluation', '')
        self_eval_scores = parse_self_evaluation(self_eval_text)
        
        correct = "Yes" if claude_correct else "No"
        
        # Create row matching the exact format from the CSV
        row = {
            'Case ID (This matches to the IDs in .json dataset)': case_id,
            'Model': 'Claude',
            'Prompt Type': 'initial',  # added to match evaluation column sheet
            'Vignette': vignette,
            'Text Output (Model Response)': claude_response,
            'Correct Diagnosis': correct_diagnosis,
            'Correct Diagnosis? (Y/N)': correct,
            'Plausibility (0/0.5/1) Human Evaluation': '',
            'Model Self-Score': self_eval_scores['plausibility'],
            'Faithfulness (0/0.5/1) Human Evaluation': '',
            'Model Self-Score.1': self_eval_scores['faithfulness'],
            'Calibration (0/0.5/1) Human Evaluation': '',
            'Model Self-Score.2': self_eval_scores['calibration'],
            'Harmfulness (0/0.5/1) Human Evaluation': '',
            'Model Self-Score.3': self_eval_scores['harmfulness'],
            'Accuracy Score': '',
            'Reasoning Quality (1–5)': '',
            'Incorrect Reasoning Type (if any)': '',
            'Hallucinations? (Y/N)': '',
            'Notes/Comments': ''
        }
        
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    if output_excel_path is None:
        input_path = Path(json_file_path)
        output_excel_path = input_path.parent / f"{input_path.stem}_output.xlsx"
    
    df.to_excel(output_excel_path, index=False, engine='openpyxl')
    
    print(f"Excel file created successfully: {output_excel_path}")
    print(f"Total cases processed: {len(rows)}")
    
    return df


if __name__ == "__main__":
    # Replace with path to JSON file generated from 'claude_auto_api_self_eval.py' 
    json_file = "claude_responses_with_self_eval_chain-of-thought.json"
    
    # Convert to Excel
    df = convert_json_to_excel(json_file)
    