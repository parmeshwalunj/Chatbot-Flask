from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from bs4 import BeautifulSoup
import os
import random
import requests
import re
import json
import urllib.request
import datetime
import webbrowser

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Parmesh123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

contractions = {"ain't": "am not", "aren't": "are not", "can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he would", "he'll": "he will", "he's": "he is", "how'd": "how did", "how'll": "how will", "how's": "how is", "i'd": "I would", "i'll": "I will", "i'm": "I am", "i've": "I have", "isn't": "is not", "it'd": "it would", "it'll": "it will", "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have", "mightn't": "might not", "must've": "must have", "mustn't": "must not", "needn't": "need not", "o'clock": "of the clock", "oughtn't": "ought not", "shan't": "shall not", "sha'n't": "shall not", "she'd": "she would", "she'll": "she will", "she's": "she is", "should've": "should have", "shouldn't": "should not", "so've": "so have", "so's": "so is", "that'd": "that would", "that's": "that is", "there'd": "there would", "there's": "there is", "they'd": "they would", "they'll": "they will", "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would", "we'll": "we will", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what're": "what are", "what's": "what is", "what've": "what have", "where's": "where is", "where've": "where have", "who'll": "who will", "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "would've": "would have", "wouldn't": "would not", "y'all": "you all", "you'd": "you would", "you'll": "you will", "you're": "you are", "you've": "you have"}
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
def check1(qs):
    text = qs
    for word in text.split():
        if word.lower() in contractions:
            text = text.replace(word, contractions[word.lower()])
    return check2(text)

def check2(qs):
    with open('F:/PythonProject/ChatBotV2/website/data.json') as jsonfile:
        data1 = json.load(jsonfile)   
        txt = qs.lower()     
        if re.search('how are you',txt) or re.search('how is it going',txt) or re.search('how are you doing',txt) or re.search('what is up',txt):
            answer = random.choice(data1['resp01'])
        elif re.search('you a robot',txt) or re.search('is this a robot',txt):
            answer = random.choice(data1['resp02'])
        elif re.search('what is your name',txt) or re.search('what is ur name',txt):
            answer = random.choice(data1['resp03'])
        elif re.search('who are you',txt) or re.search('who r u',txt):
            answer = random.choice(data1['resp03'])
        elif re.search('good bye',txt) or re.search('thank you',txt) or re.search('thanks',txt) or re.search('bye',txt):
            answer = random.choice(data1['resp04'])
        elif re.search('what can u do',txt) or re.search('what can you do',txt) or re.search('how can u help me',txt) or re.search('how can you help me',txt) or re.search('i have a question',txt) or re.search('can u help me',txt) or re.search('can you help me',txt):
            answer = random.choice(data1['resp05'])
        elif re.search('joke',txt):
            answer = random.choice(data1['resp06'])
        elif (re.search('how',txt) and re.search('old',txt) and re.search('you',txt)) or (re.search('what',txt) and re.search('your',txt) and re.search('age',txt)):
            answer = random.choice(data1['resp07'])
        elif (re.search('who',txt) and re.search('made',txt) and re.search('you',txt)) or (re.search('who',txt) and re.search('created',txt) and re.search('you',txt)) or (re.search('who',txt) and re.search('invented',txt) and re.search('you',txt)):
            answer = random.choice(data1['resp08'])
        elif (re.search('find location',txt)):
            location = txt.replace('find location', '')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get(chrome_path).open(url)
            answer = 'Here is the location of ' + location
        else:
            answer = None
        if(answer==None):
            return respond(qs)
        else: 
            return(answer)

def respond(qs):
    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.findAll("a")
    # print(links)
    all_links = []
    for link in links:
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))
    flag = False
    for link in all_links:
        if 'https://en.wikipedia.org/wiki/' in link:
            wiki = link
            flag = True
            break

    div0 = soup.find_all('div',class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3  = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

    if len(div0)!=0:
        answer = div0[0].text
    elif len(div1) != 0:
        answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
    elif len(div2) != 0:
        answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
    elif len(div3)!=0:
        answer = div3[1].text
    elif flag==True:
        page2 = requests.get(wiki)
        soup = BeautifulSoup(page2.text, 'html.parser')
        title = soup.select("#firstHeading")[0].text
    
        paragraphs = soup.select("p")
        for para in paragraphs:
            if bool(para.text.strip()):
                answer = title + "\n" + para.text
                break
    else:
        answer = "Sorry. I could not find the desired results."
    if "how to" in qs.lower():
        text1 = " #Here are some YouTube links for you:#"
        x = qs.split()
        listToStr = '+'.join([str(elem) for elem in x])
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+listToStr)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        # for i in range(3):
        link = " https://www.youtube.com/watch?v=" + video_ids[0]
        # answer = answer + '\n'
        answer = answer + text1 + link        
        # s = answer.splitlines(True)
        # lts = ''.join([str(elem) for elem in s])
        # answer = lts 
    else:
        pass
    return(answer)

def wishme():
    currentTime = datetime.datetime.now()
    currentTime.hour
    if currentTime.hour < 12:
        wish = 'Good morning'
    elif 12 <= currentTime.hour < 18:
        wish = 'Good afternoon'
    else:
        wish = 'Good evening'
    return wish