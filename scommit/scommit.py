import os
import json
import subprocess
from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI
import requests
import torch
import tiktoken
import argparse


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

def generate_commit_message_mistral(diff):
    """Generate commit message using Mistral AI."""
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    tokens = tokenizer.encode(diff)
    tokens = tokens[:7999]
    diff = tokenizer.decode(tokens)
    prompt = "You are given the output of a git diff. Your task is to create a descriptive commit message based on this diff, max 15 words\n\n" + diff
    data = {
        "model": "mistral",
        "prompt": "{prompt}".format(prompt=prompt),
        "stream": False,
    }
    response = requests.post("http://localhost:11434/api/generate", json=data)
    json_strings = response.text.strip().split('\n')
    responses = [json.loads(js)["response"] for js in json_strings]
    result = "".join(responses)
    print("Commit message: ", result)

    return result
    
def wip_hf_mistral2(diff):
    """Generate commit message using Mistral AI."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # TODO: My pc dies here lol
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

    tokens = tokenizer.encode(diff)
    tokens = tokens[:7999]
    diff = tokenizer.decode(tokens)
    prompt = "Create a commit message based on this diff, max 15 words\n\n" + diff
    data = {
        "model": "mistral",
        "prompt": "{prompt}".format(prompt=prompt),
    }
    model_inputs = tokenizer([prompt], return_tensors="pt").to(device)
    model.to(device)
    generated_ids = model.generate(**model_inputs, max_new_tokens=100, do_sample=True)
    result = tokenizer.batch_decode(generated_ids)[0]
    print("Commit message: ", result)
    x = input("Press enter to continue")
    return result

def generate_commit_message_gpt(diff):
    """Generate commit message using OpenAI's ChatGPT."""

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')

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
    """Perform a git commit with a generated or provided message."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str, help='Commit message')
    parser.add_argument('-mi', action='store_true', help='Using mistral')
    args, unknown = parser.parse_known_args()

    try:
        # Check if there are any commits
        subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD'], text=True).strip()
        commits_exist = True 
    except subprocess.CalledProcessError:
        commits_exist = False

    if commits_exist and args.mi:
        diff = subprocess.check_output(['git', 'diff', 'HEAD'] + unknown, text=True).strip()
        print(diff)
        message = generate_commit_message_mistral(diff)
        message = message.replace('"', '\\"')
    
    elif args.m is None and commits_exist:
        diff = subprocess.check_output(['git', 'diff', 'HEAD'] + unknown, text=True).strip()
        message = generate_commit_message_gpt(diff)

    else:
        message = args.m if args.m is not None else 'Initial commit'

    cmd = f'git commit {" ".join(unknown)} -m "{message}"'
    os.system(cmd)
    

if __name__ == '__main__':
    scommit()