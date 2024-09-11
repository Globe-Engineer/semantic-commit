# Semantic Commit (scommit)

Semantic Commit (scommit) is a Python script that uses the ChatGPT API to auto-generate commit messages for your git commits. You can use it exactly like `git commit`:

```bash
scommit
```

is equivalent to:

```bash
git commit -m "auto-generated commit message"
```

You can also use all of the args you normally would with `git commit`, for example:

```bash
scommit -a
```

is equivalent to:

```bash
git commit -a -m "auto-generated commit message"
```

Think of `scommit` as an alias for `git commit` that appends `-m "message"` with an auto-generated message. That's it! I recommend using this when you don't actually care about commit messages, but want them to be slightly more informative than "sdflskdjafks". Plus, it uses more GPU's than regular commits, and we all know GPU usage is a proxy for agency.

In addition, you can use the `-mi` option with `scommit` to run it locally using Ollama. For example:

```bash
scommit -mi
```

This will run `scommit` locally using Ollama instead of making a request to the ChatGPT API.

## Using the `gasp` command

The `gasp` command is a convenient way to perform `git add .`, `scommit`, and `git push` in one go. To use it, simply run:

```bash
scommit gasp
```

or

```bash
scommit --gasp
```

This will add all changes, generate a commit message, and push the changes to the remote repository.

## Installation

```bash
pip install semantic-commit
```

You should get command-line tool called `scommit` that you can use just like git commmit.

You also need to set your [OpenAI API key](https://platform.openai.com/account/api-keys) as an environment variable named OPENAI_API_KEY for scommit to work. Add this line in your `.bashrc` or `.zshrc`:

```bash
export OPENAI_API_KEY=your-api-key
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.

---

Made by Ivan Yevenko, Brian Machado and Parth Sareen
