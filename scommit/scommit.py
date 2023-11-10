import os
import sys
import json
import subprocess

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
import tiktoken


tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')

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

    tokens = tokenizer.encode(diff)
    tokens = tokens[:15900]
    diff = tokenizer.decode(tokens)
    prompt = "Can you commit this diff for me:\n\n" + diff

    response = client.chat.completions.create(messages=[
        {'role': 'system', 'content': "You call the git commit function with short and informative commit messages"},
        {'role': 'user', 'content': prompt},
    ],
    functions=[commit_schema],
    function_call={'name': 'git_commit'},
    model='gpt-3.5-turbo-16k',
    temperature=0.5)
    args = json.loads(response.choices[0].message.function_call.arguments)
    commit_message = args['commit_message']
    return commit_message


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

    unknown = [u if ' ' not in u else f'"{u}"' for u in unknown]
    cmd = f'git commit {" ".join(unknown)} -m "{message}"'
    os.system(cmd)
    

if __name__ == '__main__':
    scommit()