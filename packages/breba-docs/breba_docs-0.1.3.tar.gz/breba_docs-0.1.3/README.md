# Breba Docs

_AI documentation validator_ 

![workflow](https://github.com/breba-apps/breba-docs/actions/workflows/test.yaml/badge.svg?branch=main)

## Features
Scans your documentation file and executes commands in the documentation
to make sure that it is possible to follow the documentation.

## Prerequisites
Docker engine needs to be installed and running. Use docker installation instructions for your system.

Get OpenAI API Key and set environment variable like this:
```bash
export OPENAI_API_KEY=[your_open_ai_api_key]
```

## Getting Started

To install breba-docs, run the following commands:

```bash
pip install breba-docs
breba_docs
```

Then you will need to provide location of a documentation file. 
For example: `breba_docs/sample_doc.md`

The software will then analyze the documentation and run the commands found in the documentation
inside a docker container with python installed.

The AI will then provide feedback regarding how it was able to follow the instructions.
