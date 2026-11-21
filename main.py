import os
import argparse
import json
import re
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions, call_function

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
    for _ in range(20):
        content = generate_content(client, messages, args.verbose)
        if content is not None:
            print(content)
            return
    print("Agent took too long")
    sys.exit(1)
        
def generate_content(client, messages, verbose):
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=messages, # type: ignore
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("Failed API request.")

    if verbose is True:
        print(f"User prompt: {messages[-1]["content"]}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)
    if not message.tool_calls:
        return message.content
    for tool_call in message.tool_calls:
        message_result = call_function(tool_call, verbose)
        if verbose:
            print(f"-> {message_result['content']}")
        messages.append(message_result)
    return None

if __name__ == "__main__":
    main()
