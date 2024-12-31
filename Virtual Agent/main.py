from flask import Flask,render_template,jsonify,request
from SentimentAnalyser import SentimentAnalyser
from Chatbot import Chatbot
from config import packageDir

app = Flask(__name__)

# Set the url pattern (root access to the server) to load the index page
@app.route('/')
def index():
    return render_template('index.html') 

# Testing of the Affectiva APK
@app.route('/affectivaTests')
def affectivaTestPage():
    return render_template('affectivaTests.html')

# Testing of the applicatins Javascript 
@app.route('/jasmineTests')
def jasmineTestPage():
    return render_template('tests.html') 

# Url pattern designed to retrieve a POST request from the index web page
# Retrieve a message and an emotion  from the user and generate an apporiate responce.
@app.route('/generateMessage',methods=['GET', 'POST'])
def generateMessage():
    # extract post variables and set values to local variables
    message = request.args.get('userMessage')
    facialEmotion = request.args.get('emotion')
    chatbotType = request.args.get('chatType')
    
    # validate emotion passed from user (set to None if not set to prevent a potential TypeError)
    if not len(facialEmotion) >= 1:
        facialEmotion = "None"
        
    #perform sentiment analysis 
    messageSentiment = calculateSentimentScore(message)
    emotionSentiment = convertEmotionToSentiment(facialEmotion)
    
    # Chatbot personalites logic
    if chatbotType == "normalChatbot":
        # generate responce without the influence of affective computing techniques
        reply = recieveChatbotReply(message, None, None)
    elif chatbotType == "sentimentChatbot":
        # generate responce with the influence of Sentiment analysis only
        reply = recieveChatbotReply(message, None, messageSentiment.lower())
    elif chatbotType == "emotionChatbot":
        # generate responce with the influence of emotion recognition and sentiment analysis
        reply = recieveChatbotReply(message, emotionSentiment.lower(), messageSentiment.lower())
    
    #return chatbot message as a JSON
    return jsonify(reply)

# Ensure message does not contain inappropirate language. 
# Return true when the message does contain inappropirate language and false when it dosent
# Checking a bank of inappropirate language to search for a match
def validateAppropirateLanguage(message):
    data = open(""+packageDir+"/static/badwords.txt", "r")
    for word in data:
        if  not message.find(word.rstrip().lower()) == -1:
            print(word.rstrip())
            return False
    return True

# Generate a chatbot reply and apply the apporiate affective computing techniqiues
# Validate message based on expected sentiment (if required) and appropirate language
def recieveChatbotReply(userSentence, userFacialEmotion, userSentiment):
    
    responces = 3
    responceIterator = 0
    # Generate chatbot responce and calculate an expected sentiment responce
    chatbot = Chatbot()
    message = chatbot.test(userSentence, responces)
    messageSentiment = calculateSentimentScore(message)
    message = checkMessageLength(message)
    
    # Chatbot personaltiy 1 (No affective techniques)
    if userFacialEmotion == None and userSentiment == None:
        while validateAppropirateLanguage(message) == False:
            if(responceIterator % 3 == 0):
                responces += 1
            message = chatbot.test(userSentence, responces)
            responceIterator += 1
        return message
    # Chatbot personaltiy 2 (Sentiment Analysis)
    elif userFacialEmotion == None:
        expectedSentiment = predictExpectedMessageSentiment("", userSentiment)
    # Chatbot personaltiy 3 (Sentiment Analysis and Emotion Recognition)
    else:
        expectedSentiment = predictExpectedMessageSentiment(userFacialEmotion, userSentiment)
    
    # Generate message for chatbot 2 and 3 - Ensuring the message contains the correct sentiment before sending
    while(messageSentiment.lower() != expectedSentiment.lower() or validateAppropirateLanguage(message) == False):
        if(responceIterator % 3 == 0):
            responces += 1
        message = chatbot.test(userSentence, responces)
        messageSentiment = calculateSentimentScore(message)
        message = checkMessageLength(message)
    return message
        
    
# Performing sentiment analysis on a users message, retrieving a string output (Postive, Neutral or Negative)
def calculateSentimentScore(message):
    sentimentalAnalyser = SentimentAnalyser()
    return sentimentalAnalyser.sentimentScores(message)

# Validates the chatbots messages, when the chatbot does not generate a message, send a default message.
def checkMessageLength(message):
    if len(message) > 0 or message != "":
        return message
    message = "I'm sorry, I didn't understand you. Please talk as clearly as you possibly can."
    return message

# Collect the sentiment and facial emotional values and create a singular value (sum of both)
# To create a recommended sentiment polarity for the chatbots next message 
def predictExpectedMessageSentiment(userFacialEmotion, userSentiment):
    if(userFacialEmotion != "negative" and userFacialEmotion == userSentiment):
        overallSentiment = userFacialEmotion
    else:
        if(userFacialEmotion == "positive" or userSentiment == "positive"):
            overallSentiment = "positive"  
        
        elif(userFacialEmotion == "negative" or userSentiment == "negative"):
            overallSentiment = "neutral"
        else:
            overallSentiment = "neutral"
    return overallSentiment

# Convert emotion (passed from scripts.js) language to use the same language as the sentiment analyser
# To ensure values can be accuractly compared and the values are restricted to three consistent values
# positive, neutral and negative
def convertEmotionToSentiment(emotion):
    if emotion == "joy":
        emotion = "positive"
    elif emotion == "contempt" or emotion == "surprise":
        emotion = "neutral"
    elif emotion == "fear" or emotion == "anger" or emotion == "disgust" or emotion == "sad":
        emotion = "negative"
    else:
        emotion = "neutral"
    return emotion 


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)