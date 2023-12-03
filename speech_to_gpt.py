import speech_recognition as sr

'''make sure to create an environment variable: OPENAI_API_KEY
Otherwise you'll receive an error back from OpenAI.
You must have a paid for subscription to use this otherwise
you'll receive quota errors.''' 

def transcribe_speech(microphone, recognizer):
    '''takes a recording, and transcribes it, 
    reporting back if the recording was successful
    
    :param microphone: sr.Microphone instance
    :param recognizer: sr.Recognizer instance
    :return transcription dict: transcription dictionary'''

    if not isinstance(microphone, sr.Microphone):
        raise TypeError('microphone must be sr.Microphone instance')
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError('recognizer must be sr.Recognizer instance')
    
    response = {
        'success': True,
        'transcription': None,
        'error': None
        }
    
    with microphone as source:
        print('adjusting...')
        recognizer.adjust_for_ambient_noise(source)
        print('speak now...')
        audio = recognizer.listen(source)

    try:
        response['transcription'] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response['success'] = False
        response['error'] = 'API Request Error'
    except sr.UnknownValueError:
        response['error'] = 'Unable to recognize speech'

    return response

if __name__ == '__main__':
    from langchain.prompts import ChatPromptTemplate
    from langchain.chat_models import ChatOpenAI

    template = ''''You are a helpful assistant from the world of Douglas Adams
    and the hitchikers guide to the galaxy, you assume this role and don't deviate
    or move from it. you will ONLY respond in this character. A user will ask
    a question and you must respond with the answer to that question. Check your workings
    and ensure that you stay in the style of Douglas Adams throughout.'''
    human_template = '{text}'

    chat_prompt = ChatPromptTemplate.from_messages([
        ('system', template),
        ('human', human_template)
    ])

    hiker_answer_chain = chat_prompt | ChatOpenAI(model_name='gpt-3.5-turbo')

    sound_recorder = sr.Microphone()
    recogniser = sr.Recognizer()

    speech_success = True
    
    for i in range(5):
        print("Let's record a question for Douglas Adams")
        recorded = transcribe_speech(sound_recorder,recogniser)

        if not recorded['success']:
            print(f"ERROR: {recorded['error']}")
            break

        elif recorded['error']:
            print(f"Please try again, I didn't catch that")
        
        else:
            print('asking Douglas Adams...')
            print(recorded['transcription'], '?')

            llm_response = hiker_answer_chain.invoke({'text': recorded['transcription']}).content
            print(llm_response)

            from openai import OpenAI
            import os
            api_key = os.environ['OPENAI_API_KEY']
            client = OpenAI(api_key=api_key)

            # TODO: add streaming generation. 
            # generate speech from the text
            response = client.audio.speech.create(
            model="tts-1", # the model to use, there is tts-1 and tts-1-hd
            voice="onyx", # the voice to use, there is alloy, echo, fable, onyx, nova, and shimmer
            input=llm_response, # the text to generate speech from
            speed=1.0, # the speed of the generated speech, ranging from 0.25 to 4.0
            )
            # save the generated speech to a file
            response.stream_to_file("doug-adams-onyx.mp3")

            # TODO: add speech playback, some other methods stored below.
                
            # import gtts
            # tts = gtts.gTTS(llm_response)
            # tts.save('llm_response.mp3')

            # import pyttsx3
            # engine = pyttsx3.init()
            # engine.say(llm_response)
            # engine.runAndWait()
            break

    

