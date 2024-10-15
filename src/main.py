#!/usr/bin/python

import os
import openai
from dotenv import dotenv_values

# Set up OpenAI credentials
CONFIG = dotenv_values(".env")

OPEN_AI_KEY = CONFIG.get("KEY") or os.getenv("OPEN_AI_KEY")
OPEN_AI_ORG = CONFIG.get("ORG") or os.getenv("OPEN_AI_ORG")

openai.api_key = OPEN_AI_KEY
openai.organization = OPEN_AI_ORG

def load_file(filename: str = "") -> str:
    """Loads an arbitrary file name."""
    try:
        with open(filename, "r") as fh:
            return fh.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return ""

def save_to_file(filename: str, content: str):
    """Saves the generated content to a file."""
    with open('../writing/text.md', 'w') as f:
        f.write("# Chain of Thought Analysis\n\n")
        f.write(content)

def generate_chain_of_thought_analysis(source_text: str) -> str:
    """Generates a step-by-step critical analysis using GPT's chain of thought prompting."""
    messages = [
        {"role": "system", "content": "You are a critical text analyst."},
        {"role": "user", "content": (
            "Analyze the following text using a step-by-step chain of thought reasoning. "
            "Focus on uncovering hidden structures, subtle word relationships, and deeper meanings. "
            "At each step, explain the reasoning behind your observations.\n\n"
            f"Text: {source_text}\n\n"
            "Start your critical breakdown below:"
        )}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=750,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "An error occurred during the GPT response."

def main():
    # Load source file
    source_text = load_file("data/source.txt")

    if not source_text:
        print("Source text is empty or could not be loaded.")
        return

    # Generate chain of thought analysis
    analysis = generate_chain_of_thought_analysis(source_text)

    # Save the analysis to the output file
    output_filename = "writing/text.md"
    save_to_file(output_filename, f"# Chain of Thought Analysis\n\n{analysis}")

    print(f"Analysis saved to {output_filename}")

if __name__ == "__main__":
    main()