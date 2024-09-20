from database import save,row_exists,login_details
import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from flask import Response

from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    if ints:
        tag = ints[0]['intent']
        print(tag)
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            print(i["tag"])
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result
    else:
        return "Sorry, I didn't understand that."

def chatbot_response(msg):
    if msg.lower() == "male":
        return "Welcome Mr please select your age"
    elif msg.lower() == "female":
        return "Welcome Mrs please select your age"

    elif msg.lower() == "adolescentage":
        return "Thank you for selecting your age category. Your response has been noted"
    
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
        return res



from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

@app.route('/login',methods=["GET","POST"])
def log():
    if request.method=="POST":
        name=request.form["name"]
        pas=request.form["password"]
        str1=login_details(name,pas)
        print(str1)
        if name == "" or pas == "":
            return render_template('login.html', mandatory_message="credentials are empty")
            #return Response("All fields are mandatory")
        else:    
            if str1==True:
                return render_template('index.html')
            else:
                return render_template('login.html', invalid_message="Invalid credentials")
           # return Response('Invalid credentials')
    else:
        return render_template('login.html')

@app.route('/register',methods=["GET","POST"])
def reg():
    if request.method == "POST":
        name = request.form["name"]
        pas = request.form["password"]
        if name == "" or pas == "":
            return render_template('register.html', mandatory_message="All fields are mandatory")
            #return Response("All fields are mandatory")
        else:
            str1 = row_exists(name)
            if str1 == False:
                save(name, pas)
                return render_template('register.html', success_message="Registration successful!")
            else:
                return render_template('register.html', error_message="Username already taken")
                #return Response("Username already taken")
    else:
        return render_template('register.html')
if __name__ == "__main__":
    app.run(debug=True)