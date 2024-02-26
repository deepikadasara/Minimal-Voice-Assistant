
from flask import Flask, render_template, jsonify
import speech_recognition as sr
import random
import logging
from gtts import gTTS
import os
from flask import Flask, render_template

app = Flask(__name__)

# Initialize the speech recognizer 
recognizer = sr.Recognizer()

# Define a list of possible questions
# Function to read questions from the text file
def read_questions(filename):
    questions = []
    with open(filename, 'r') as file:
        for line in file:
            questions.append(line.strip())
    return questions

# Read questions from the text file
questions = read_questions('questions.txt')

def text_to_speech(text):
    # Initialize gTTS with the text to convert
    speech = gTTS(text)

    # Save the audio file to a temporary file
    speech_file = 'speech.mp3'
    speech.save(speech_file)

    # Play the audio file
    os.system('afplay ' + speech_file)

def ask_question():
    # Select a random question from the list
    question = random.choice(questions)
    # Speak the question
    text_to_speech(question)
    return question

def listen_answer(question):
    # Listen for the answer
    with sr.Microphone() as source:
        # Adjust the noise level
        recognizer.adjust_for_ambient_noise(source,duration=2)
        text_to_speech('Start speaking now-')
        # Record the audio
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)
    # Try to recognize the answer
    try:
        # Use the default speech recognition API
        answer = recognizer.recognize_google(audio)
        # Return answer
        return answer
    except sr.UnknownValueError:
        # If the answer is not recognized, return None
        return None

def handle_response(question):
    # function to process and log response
    def process_log_response(answer,question):

        # Speak a confirmation message
        text_to_speech(f"You said {answer}.")

        # Log the question and answer
        logging.info(f"Question: {question}")
        logging.info(f"Answer: {answer}")
    
    # Define a function to validate the response
    def validate_response(answer):
        if answer is not None:
            # Convert the answer to lower case
            answer = answer.lower()
            # If the answer is yes or no
            if answer == "yes" or answer == "no":
                return True, answer
        return False, None

    # Initialize attempts counter
    attempts = 0
    valid_response = False
    while valid_response==False and attempts < 3:
        answer = listen_answer(question)
        valid_response, validated_answer = validate_response(answer)
        if not valid_response:
            attempts += 1
            process_log_response(f"Invalid Response-{answer}",question)
            if answer==None:
                text_to_speech("Sorry, I didn't get that. Please respond with yes or no.")
            else:
                text_to_speech("Invalid Answer. Please respond with yes or no.")
        else:
            answer = validated_answer
            break

    # If the response is still not valid after three attempts
    if not valid_response:
        text_to_speech("Invalid response after 3 attempts.")
        return
    else:
        process_log_response(answer,question)



@app.route('/')
def index():
    return render_template('index_test.html')


@app.route('/assistant')
def run_voice_assistant():
    # Set up the logging configuration
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    logging.basicConfig(filename="voice_assistant.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    # Speak a welcome message
    text_to_speech("Hello, I am a voice assistant at VirtuSense. I will ask you a single, creative question that expects a yes or no answer. Please respond when instructed.")
    question = ask_question()

    # Handle the response
    handle_response(question)

    # Speak a goodbye message
    text_to_speech("Thank you for your time. Goodbye.")

    return jsonify({'response': "Voice assistant session completed. Check the log for details."})

   
if __name__ == '__main__':
    app.run(debug=True)
