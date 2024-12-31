import pytest,inspect, os, sys
sys.path.append("..")
from config import packageDir
sys.path.insert(0,packageDir)
from main import *

def test_sentiment_analysis():
    assert calculateSentimentScore("Shut up, I HATE you") == "Negative"
    assert calculateSentimentScore("The sky is normal") == "Neutral"
    assert calculateSentimentScore("This conversation is the best") == "Positive"

def test_predicted_expected_message_sentiment():
    assert predictExpectedMessageSentiment("positive","positive") == "positive"
    assert predictExpectedMessageSentiment("positive","neutral") == "positive"
    assert predictExpectedMessageSentiment("positive","negative") == "positive"
    assert predictExpectedMessageSentiment("neutral","positive") == "positive"
    assert predictExpectedMessageSentiment("negative","positive") == "positive"
    assert predictExpectedMessageSentiment("neutral","negative") == "neutral"
    assert predictExpectedMessageSentiment("negative","neutral") == "neutral"
    assert predictExpectedMessageSentiment("negative","negative") == "neutral"

def test_emotion_to_sentiment():
    assert convertEmotionToSentiment("joy") == "positive"
    assert convertEmotionToSentiment("contempt") == "neutral"
    assert convertEmotionToSentiment("surprise") == "neutral"
    assert convertEmotionToSentiment("fear") == "negative"
    assert convertEmotionToSentiment("anger") == "negative"
    assert convertEmotionToSentiment("disgust") == "negative"
    assert convertEmotionToSentiment("sad") == "negative"

def test_appropirate_lanage_check():
    assert validateAppropirateLanguage("This message contains no negative language") == True
    assert validateAppropirateLanguage("This message contains one bad word - ass") == False

def test_check_message_length():
    assert checkMessageLength('') == "I'm sorry, I didn't understand you. Please talk as clearly as you possibly can."
    assert checkMessageLength('Hey how are you?') == 'Hey how are you?'

def test_recieve_chatbot_reply():
    message = recieveChatbotReply('Hey how are you?', "positive", "negative")
    assert len(message) > 0
    assert validateAppropirateLanguage(message) == True    
