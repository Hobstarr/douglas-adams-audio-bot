<center> <img src="https://github.com/Hobstarr/s2t-gpt-t2s-douglas-adams/assets/56070935/6b0d2fa5-115b-49bc-8966-1cf327a2818d" width="4800" height="240" align='center'> </center>

# Douglas Adams Bot - interaction through speech.

### speech to text, custom gpt template, text to speech. #langchain / openai.

Simple question-answering CLI bot that uses Douglas Adams character to respond. 

The script uses speech recognition to listen to a query from a user.
The audio is then transcribed and then passed to a custom Douglas Adams themed openai call.
The response is received and processed to audio as 'doug-adams-onyx.mp3' (as it uses the onyx voice).

to run simply: 

``` python speech_to_gpt.py ```


### setting up environment: 
Setting up environment, this was built using python 3.11.6 and pip 23.3.1. 
Build a virtual environment:

``` python venv .venv ```

Activate .venv and install requirements:

``` pip install -r requiements.txt ```

You will need an [openai paid account / API key](https://platform.openai.com/api-keys):


Set your openai_api_key variable (replace ... with your api key):

``` export OPENAI_API_KEY='...' ```
