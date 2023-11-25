import os
import sys
import json
import subprocess
from transformers import AutoTokenizer 
from requests import Response
from openai import OpenAI

# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
import tiktoken


tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')
tokenizer2 = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

commit_schema = {
    "name": "git_commit",
    "description": 'Performs a git commit by calling `git commit -m "commit_message"`',
    "parameters": {
        "type": "object",
        "properties": {
            "commit_message": {
                "description": "A short but descriptive commit message",
                "type": "string"
            }
        },
        "required": ["commit_message"]
    }
}

def generate_commit_message(diff):
    if len(diff) == 0:
        return 'default commit message'

    tokens = tokenizer2.encode(diff)
    # tokens = tokens[:15900]
    tokens = tokens[:7000]
    diff = tokenizer2.decode(tokens)
    prompt = "Create a commit message based on this diff, max 15 words\n\n" + diff

    # response = client.chat.completions.create(messages=[
    #     {'role': 'system', 'content': "You call the git commit function with short and informative commit messages"},
    #     {'role': 'user', 'content': prompt},
    # ],
    # functions=[commit_schema],
    # function_call={'name': 'git_commit'},
    # # model='gpt-3.5-turbo-16k',
    # model='mistral',
    # temperature=0.5)

    # args = json.loads(response.choices[0].message.function_call.arguments)
    # commit_message = args['commit_message']
    import requests
    data = {
        "model": "mistral",
        "prompt": "{prompt}".format(prompt=prompt),
    }
    response = requests.post("http://localhost:11434/api/generate", json=data)

    # commit_message = response.json()['commit_message']
    print(response)
    print(response.text)
    import json



    json_strings = response.text.strip().split('\n')

    responses = [json.loads(js)["response"] for js in json_strings]
    print(responses)
    result = "".join(responses)

    print(result)  # Outputs: "1. Hello"
    # print(response.json())
    # return commit_message
    return result


def scommit():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str, help='Commit message')
    args, unknown = parser.parse_known_args()

    try:
        # Check if there are any commits
        subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD'], text=True).strip()
        no_commits = False
    except subprocess.CalledProcessError:
        no_commits = True

    if args.m is None and not no_commits:
        diff = subprocess.check_output(['git', 'diff', 'HEAD'], text=True).strip()
        message = generate_commit_message(diff)
    else:
        message = args.m if args.m is not None else 'Initial commit'

    message = message.replace('"', '\\"')

    cmd = f'git commit -a -m "{message}"'
    print(cmd)
    os.system(cmd)
    

if __name__ == '__main__':
    scommit()