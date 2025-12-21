import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    print("Hello from aiagent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("missing api key")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.usage_metadata != None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("no usage metadata found")

    # if response.function_calls != None:
    #     for function_call in response.function_calls:
    #         print(f"Calling function: {function_call.name}({function_call.args})")
    # else:
    #     print(response.text)

    response_list = []
    if response.function_calls != None:
        for function_call in response.function_calls:
            response = call_function(function_call)
            if not response.parts[0].function_response.response:
                raise Exception("error: no response")
            else:
                response_list.append(response.parts[0])
                print(f"Calling function: {function_call.name}({function_call.args})")
                if args.verbose:
                    print(f"-> {response.parts[0].function_response.response}")


if __name__ == "__main__":
    main()
