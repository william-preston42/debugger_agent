import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("No API key found.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ],
)

def token_usage() -> str | None:
    if response.usage is None:
        raise RuntimeError("Failed API request.")
    return f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}"

def agent_message():
    return f"Response:\n{response.choices[0].message.content}"

def main():
    print(token_usage())
    print(agent_message())

if __name__ == "__main__":
    main()
