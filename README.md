Voice Assistant Application Documentation
Live Demo: https://drive.google.com/file/d/1CzVK_1R0Las1zmYzZzGEwzSTwLn4-jQL/view?usp=sharing

<img width="1024" alt="Screenshot 2024-02-26 at 2 03 02 AM" src="https://github.com/deepikadasara/Minimal-Voice-Assistant/assets/47112406/64ac60cb-4398-40c9-a8eb-486996537776">


The Voice Assistant Application is a conversational agent designed to interact with users through voice commands. It asks users creative questions and processes their verbal responses. The application leverages the speech_recognition library for speech-to-text conversion, the gTTS (Google Text-to-Speech) library for text-to-speech synthesis, and standard Python libraries such as random for question selection and logging for maintaining logs of the interaction.
Features
Speech Recognition: Utilizes the speech_recognition library to accurately interpret user responses and handles noise.
Text-to-Speech: Converts text messages to speech using the gTTS library, providing an interactive experience.
Question Randomization: Selects a creative question randomly from a predefined list to ask the user.
Response Validation: Validates user responses to ensure they are within expected parameters (i.e., "yes" or "no").
Logging: Records all questions asked and responses received for auditing or review purposes.
Workflow
Initialization: The application initializes the speech recognizer and reads a list of questions from a text file. The text file contains 100 thought provoking questions requiring a yes/no response. They have been obtained from ChatGPT and have been validated.


Asking Questions: It selects a random question to ask the user and uses text-to-speech to vocalize it.


Listening to the Answer: The application captures the user's response through the microphone, converting the speech to text.


Response Handling:
Validates the user's response. If the response is not "yes" or "no," the user is prompted again, up to three attempts.
Once a valid response is received, or after three unsuccessful attempts, the application proceeds.
The response, along with the question asked, is logged.

Logging: Each interaction, including the question asked and the user's response, is logged for future reference.
Handling Background Noise and Efficiency
The speech_recognition library, used by the Voice Assistant Application, provides functionality to adjust for ambient noise, thereby improving the accuracy of speech-to-text conversion.
Adjust for Ambient Noise: The application calls the recognizer.adjust_for_ambient_noise(source) method of the speech_recognition.Recognizer class. This method analyzes the audio source for a short period to calibrate the recognizer's noise threshold. This calibration process helps the recognizer distinguish between the user's speech and background noise.
The method typically requires specifying a duration for which to listen to the ambient noise. A duration of 2 has been set which works well for environments with varying degrees of noise.
Timeouts are essential for managing the duration of listening and processing phases, preventing the application from waiting indefinitely for user input or getting stuck in a processing loop.
Speech Recognition Timeout: The recognizer.listen(source) method can be provided with a timeout parameter. This parameter defines the maximum number of seconds the recognizer will wait for speech to start before giving up. A timeout of 10 has been set.
Phrase Time Limit: In addition to the timeout parameter, the recognizer.listen() method accepts a phrase_time_limit parameter. This parameter sets the maximum duration for which the recognizer will listen to the speech, effectively limiting the length of the user's response. This limit ensures that the application does not spend excessive time processing long recordings. This has been set to 3 as the valid responses expected are yes/no which are short.


Installation Requirements
Python 3.12
brew install portaudio
requirements.txt
Setup and Execution
Install Required Libraries: Ensure all the required Python libraries are installed 
brew install portaudio
pip3 install --no-cache-dir -r requirements.txt


Prepare Questions File: Text file named questions.txt contains 100 creative questions, one per line. We can append more questions to this file if required.

Run the Application: Execute the commands to run the flask application.
export FLASK_APP=app
flask run
Interaction: The application will vocalize a greeting, ask a question, and prompt the user to respond. It will process and respond to the user's input verbally.
Logging
The application maintains a log file (voice_assistant.log) that records the datetime of each interaction, the question asked, and the user's response. This file is essential for reviewing the application's usage and auditing interactions.
Docker

I've developed a Docker container for this application using the following commands to set it up:
docker build -t my-flask-app .
docker run -p 5001:5000 my-flask-app

I'm using macOS as my operating system. However, I've encountered an issue where the Docker container isn't able to access the microphone and speakers of the host system. This limitation is preventing the application from functioning correctly.

To clarify, Docker containers are designed to run applications in isolated environments. This isolation is great for many purposes but poses a challenge for applications that need to interact with specific hardware features of the host machine, such as the microphone and speakers. In the case of macOS, Docker doesn't provide a direct method for containers to access these hardware features. This discrepancy is the root cause of the problem, leading to the application not working as intended within the Docker environment on macOS. I’ll be researching more to see ways in which this can be implemented.
