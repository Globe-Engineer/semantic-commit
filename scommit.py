import os
import sys
import json
import subprocess

import openai
import tiktoken

openai.api_key = os.environ["OPENAI_API_KEY"]
tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')

commit_schema = {
    "name": "git_commit",
    "description": 'Performs a git commit by calling `git commit -m "commit_message"`',
    "parameters": {
        "type": "object",
        "properties": {
            "commit_message": {
                "description": "A short message describing the commit",
                "type": "string"
            }
        },
        "required": ["commit_message"]
    }
}

def generate_commit_message(diff):
    tokens = tokenizer.encode(diff)
    tokens = tokens[:15900]
    diff = tokenizer.decode(tokens)
    prompt = "Generate a commit message for the following diff:\n\n" + diff
    try:
        response = openai.ChatCompletion.create(
            messages=[{'role': 'user', 'content': prompt}],
            functions=[commit_schema],
            function_call={'name': 'git_commit'},
            model='gpt-3.5-turbo-16k',
            temperature=0.5,
        )
        args = json.loads(response.choices[0]['message']['function_call']['arguments'])
        commit_message = args['commit_message']
        return commit_message
    except Exception as e:
        return 'default commit message'


def scommit():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str, help='Commit message')
    args, unknown = parser.parse_known_args()

    if args.m is None:
        diff = subprocess.check_output(['git', 'diff', '--cached'], text=True).strip()
        message = generate_commit_message(diff)
    else:
        message = args.m

    unknown = [u if ' ' not in u else f'"{u}"' for u in unknown]
    cmd = f'git commit {" ".join(unknown)} -m "{message}"'
    os.system(cmd)
    

if __name__ == '__main__':
    scommit()