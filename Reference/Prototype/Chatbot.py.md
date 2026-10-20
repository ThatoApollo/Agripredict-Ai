###### Chatbot.py:



from sklearn.feature\_extraction.text import TfidfVectorizer

from sklearn.linear\_model import LogisticRegression



\# Natural language intent classification over a small set of approved questions

examples = \[

&#x20;   ("what is the yield estimate for free state", "estimate"),

&#x20;   ("predict the maize yield for mpumalanga", "estimate"),

&#x20;   ("how much maize will north west produce", "estimate"),

&#x20;   ("what is the expected yield this season", "estimate"),

&#x20;   ("how do the provinces compare", "compare"),

&#x20;   ("which province has the highest yield", "compare"),

&#x20;   ("compare provincial yields", "compare"),

&#x20;   ("how accurate is the model", "performance"),

&#x20;   ("what is the mae and rmse", "performance"),

&#x20;   ("how well does the model perform", "performance"),

&#x20;   ("where does the data come from", "data"),

&#x20;   ("what data was used", "data"),

&#x20;   ("what are the limitations", "limitations"),

&#x20;   ("what should i be careful about", "limitations"),

&#x20;   ("can you guarantee the yield", "limitations"),

&#x20;   ("how much storage will we need", "storage"),

&#x20;   ("what production volume should we plan for", "storage"),

&#x20;   ("help me plan procurement", "storage"),

]



texts = \[text for text, \_ in examples]

intents = \[intent for \_, intent in examples]



vectorizer = TfidfVectorizer()

classifier = LogisticRegression(max\_iter=1000)

classifier.fit(vectorizer.fit\_transform(texts), intents)



\# Bounded answers, drawn only from approved project information

ANSWERS = {

&#x20;   "estimate": "AgriPredict gives a provincial average yield in tonnes per hectare. Open the dashboard and choose a province to see the estimate for the coming season.",

&#x20;   "compare": "The dashboard compares the three provinces. Free State and Mpumalanga generally give higher yields, while North West is lower on average.",

&#x20;   "performance": "The models are judged on the last four seasons using MAE and RMSE. Run yield\_model.py to print the current figures.",

&#x20;   "data": "The prototype uses historical maize production and harvested-area records together with seasonal rainfall and temperature for the three provinces.",

&#x20;   "limitations": "These are provincial averages, not farm-level predictions, and they are not guarantees. Check the model errors before making firm commitments.",

&#x20;   "storage": "Multiply the yield estimate by the harvested area you expect, to get a production volume, then compare that with your available storage.",

}



def respond(question):

&#x20;   intent = classifier.predict(vectorizer.transform(\[question]))\[0]

&#x20;   return ANSWERS\[intent]



def run\_chatbot():

&#x20;   print(open("instructions.txt").read())

&#x20;   while True:

&#x20;       question = input("You: ")

&#x20;       if question.lower() in \["quit", "exit", "bye"]:

&#x20;           break

&#x20;       print("AgriPredict:", respond(question))



if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   run\_chatbot()

