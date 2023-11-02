# ChatGPT AI Voice Assistant

![GitHub Actions Build Status](https://github.com/jakecyr/openai-gpt3-chatbot/actions/workflows/test-application.yml/badge.svg)

As an AI teacher, the application incorporates two fundamental functions: speech-to-text for input and text-to-speech for output, with the added capability of providing responses in multiple languages， and different subjects.

<img width="994" alt="Screen Shot 2023-11-02 at 11 22 40 AM" src="https://github.com/huizhezh/AI-teacher/assets/101370768/32ceef7d-2bbc-4129-b212-c4c96d62c4f1">
####


<img width="998" alt="Screen Shot 2023-11-02 at 11 09 14 AM" src="https://github.com/huizhezh/AI-teacher/assets/101370768/daadfbed-145b-4262-af02-354debb935ec">

### General Setup
Python version: 3.11 
Optionally create a new Python environment and activate it:
```bash
# create a new environment in the current directory called env
python3 -m venv env

# activate the environment
source env/bin/activate
```
## Prerequisites
```bash
# Install library: 
pip install -r requirements.txt
```

## OPENAI_API_KEY
Either set the `OPENAI_API_KEY` environment variable before running the script or pass in your secret key to the script like in the example below:
```bash
export OPENAI_API_KEY=<OPEN API SECRET KEY HERE>
# OR create .env file and enter key
OPENAI_API_KEY=<OPEN API SECRET KEY HERE>
```

## Running the Script

```bash
python main.py
```

## References

[OpenAI API docs](https://platform.openai.com/docs/quickstart?context=python)

[SpeechRecognition library docs](https://pypi.org/project/SpeechRecognition/1.2.3)

[Google Translate Text-to-Speech API (gTTS)](https://gtts.readthedocs.io/en/latest/module.html#)


