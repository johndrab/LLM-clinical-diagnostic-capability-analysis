# LLM Clinical Diagnostic Capability Analysis

A lightweight evaluation framework to assess the diagnostic reasoning quality of large language models in clinical contexts.

## Overview

This project evaluates the clinical diagnostic capabilities of three state-of-the-art general-purpose LLMs:
- **GPT-4.1** (OpenAI)
- **Claude Sonnet 4.5** (Anthropic)
- **Gemini 2.5 Flash** (Google)

The evaluation uses 50 curated clinical vignettes across three prompting strategies to measure diagnostic reasoning quality and accuracy.

## Evaluation Framework

### Prompting Strategies
1. **Zero-shot**: Direct diagnostic queries without examples
2. **Few-shot**: Diagnostic queries with example cases
3. **Chain-of-Thought (CoT)**: Step-by-step reasoning prompts

### Evaluation Dimensions
Models are assessed across four key dimensions:

- **Plausibility**: Clinical validity and appropriateness of diagnostic suggestions
- **Faithfulness**: Adherence to provided clinical information without hallucination
- **Calibration**: Accuracy of confidence levels in diagnostic predictions
- **Safety**: Identification of potential harms and appropriate caveats

## Repository Structure

```
.
├── dataset/                    # Clinical vignettes and test cases
├── Scripts/
│   └── Claude scripts/        # Evaluation scripts for Claude models
├── ECS 289G LLM Clinical Vignette Evaluations.xlsx # Evaluation results
├── Gemini_and_GPT_Scripts.ipynb              # Main analysis notebook
├── README.md                  # This file
└── Standardized Prompt Headers and Evaluation Rubric.pdf
```

## Summary
Models are assessed along four dimensions: Plausibility, Faithfulness, Calibration, and Safety. This lightweight framework enables comparison of reasoning quality and diagnostic accuracy across different LLMs.
