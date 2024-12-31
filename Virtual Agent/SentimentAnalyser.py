# Sources
# Vader Lexicon - https://www.nltk.org/api/nltk.sentiment.html
# Dataset - https://www.kaggle.com/ngyptr/python-nltk-sentiment-analysis

import csv
import vaderSentiment 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyser:
    
    #Calculate the String sentiment value of a sentance/message (parameter)  
    def sentimentScores(self,sentence):
        #Access VADER lexiocon class to utilise sentiment analysis properties and attributes
        analyser = SentimentIntensityAnalyzer()
        #Isolate the message polarity values into variables
        compoundValue = analyser.polarity_scores(sentence)['compound']
        #Utilise the compound (sum) variable to extract the numeric message polarity to a String 
        if(compoundValue >= 0.05):
            outcome = "Positive"
        elif(compoundValue < 0.05 and compoundValue > -0.05):
            outcome = "Neutral"
        elif(compoundValue < -0.05):
            outcome = "Negative"    
        #return the String version of the message polarity
        return outcome

    #Testing environment to measure the accuracy of the library
    def sentimentTesting(self):
        with open("static/sentimentDataSet.csv", "r", encoding="utf-8" ,errors='ignore', newline='') as file:
            reader = csv.reader(file)
            accuracyCount = 0
            failedCount = 0
            sentimentConfidenceCsvColumn = 6
            sentimentCsvColumn = 5
            textCsvColumn = 15
            for row in reader:
                if row[sentimentConfidenceCsvColumn] == "1" and self.sentimentScores(row[textCsvColumn]).strip() != "Neutral":
                    if row[sentimentCsvColumn].strip() == self.sentimentScores(row[textCsvColumn]).strip():
                        accuracyCount += 1
                        print("Accurate " + row[sentimentCsvColumn].strip() + " - " + self.sentimentScores(row[textCsvColumn]).strip())
                    else:
                        failedCount += 1
                        print("Failed " + row[sentimentCsvColumn].strip() + " - " + self.sentimentScores(row[textCsvColumn]).strip())
            
            print("Correct Predictions: " + str(accuracyCount))
            print("Wrong Predictions: " + str(failedCount))

    # sentimentScores("I just got a call from my boss - does he realise it's Saturday?!!! :(")
    # sentimentTesting()

    ## Sentiment Accuracy = 51%
    ## However, the dataset's neutral is quite subjective - as the dataset was created from another classifer
    ## Not counting mild (neutral) incorrect predictions the accruacy is 61%