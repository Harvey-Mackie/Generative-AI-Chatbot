# Affective Virtual Agent 

Note - this was created as my final year project at University while studying Comp Sci. 

The paper title is 'An Investigation into the effectiveness of emotionally intelligent virtual agents’ ability to showcase empathy for users' - please contact if interested in reading.

## Overview
A conversational agent that utilizes sentiment analysis and facial emotion recognition to provide empathetic responses. Built using Python, Flask, and TensorLayer.

![image](https://github.com/user-attachments/assets/51b86865-73a8-4379-abc3-e294ed8e23ae)


## Features
- Seq2Seq model for open domain conversations
- Multiple agent personalities with varying levels of emotional intelligence
- Sentiment analysis using VADER
- Real-time facial emotion recognition using Affectiva SDK
- Web-based interface for interaction

## Technical Stack
- Backend: Python, Flask
- ML Framework: TensorLayer (based on TensorFlow)
- Frontend: HTML, CSS, JavaScript (jQuery)
- Emotion Recognition: Affectiva Emotion Detection SDK
- Testing: Pytest (backend), Jasmine (frontend)

## Chatbot Model Details
- Architecture: Seq2Seq model with 3 RNN layers
- Training Data:
  - Cornell Movie Dialogs Corpus (220,579 dialogs)
  - Twitter Corpus (377,265 conversations)
- Layer Configuration: 256 units per layer
- Training Split: 70% training, 15% testing, 15% validation
![image](https://github.com/user-attachments/assets/b0c92717-64c2-4b76-9be2-9cb901b8956d)

## Virtual Agent Personalities
- Base Agent: No affective computing
- Sentiment-Aware Agent: Utilizes sentiment analysis
- Emotionally-Aware Agent: Utilizes both sentiment analysis and facial emotion recognition
![image](https://github.com/user-attachments/assets/9860956a-f4fc-4444-b2eb-ff847bddf866)

## Flow Chart
![image](https://github.com/user-attachments/assets/256091cb-4d6b-4bd5-8cbe-0cb9cb5fb8a8)

## Getting Started

- To set-up the environment for the application, ensure you have Python 3.5> installed on your machine.
- Once installed, run the following command `pip install -r requirements.txt`
- Access the config.py file in the directory root, here, alter the variable `packageDir` to the full path of the root directory (Virtual Agent)
- Open terminal/command prompt on your machine (navigate to Virtual Agent Directory), and enter the following command `py main.py` or `python main.py`, to initialise the FLASK application.
- Naviagate to the URL outined in the terminal - e.g. **127.0.0.1:5000** (root)
- Each of the Virtual Agents can be conversed with; Enjoy.

## Testing 

- The Javascript section of the application was tested utilising the Jasmine framework. To see the test logs, navigate to the url **127.0.0.1:5000/jasmineTests** - *Disclaimer - numerous tests are being carried out, thus, the page takes along time to load*.

- The Affectiva APK testing section of the application utilsies User Testing. To test, navigate to the url **127.0.0.1:5000/affectivaTests** - *Results of the testing are displayed within the footer of the page*

- The FLASK Testing section can only be carried out in the **terminal**. Enter the command `pytest`, while in the Affective Virtual Agent directory.
