# ChatGPT AI Voice Assistant

![GitHub Actions Build Status](https://github.com/jakecyr/openai-gpt3-chatbot/actions/workflows/test-application.yml/badge.svg)

As an AI teacher, the application incorporates two fundamental functions: speech-to-text for input and text-to-speech for output, with the added capability of providing responses in multiple languages， and different subjects.

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

[SpeechRecognition library docs](https://pypi.org/project/SpeechRecognition/1.2.3)

[Google Translate Text-to-Speech API (gTTS)](https://gtts.readthedocs.io/en/latest/module.html#)


