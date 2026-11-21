import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt },
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args.verbose)

def generate_content(client, messages, verbose):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages, # type: ignore
    )
    if response.usage is None:
        raise RuntimeError("Failed API request.")

    if verbose is True:
        print(f"User prompt: {messages[-1]["content"]}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
    print(f"Response:\n{response.choices[0].message.content}")

if __name__ == "__main__":
    main()
