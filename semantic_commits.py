import os
import sys
import json
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
            model='gpt-3.5-turbo-16K',
            temperature=0.5,
        )
        args = json.loads(response.choices[0]['message']['function_call']['arguments'])
        commit_message = args['commit_message']
        print(commit_message)
    except Exception as e:
        print('default commit message')

    

if __name__ == '__main__':
    diff = sys.argv[1]
    generate_commit_message(diff)