import pandas as pd
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

options = Options()
options.headless = True
service = Service(executable_path="chromium.chromedriver")
b = webdriver.Chrome(options=options, service=service)

import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)
df = pd.read_csv("main.csv")
# df = pd.read_csv("main.csv",thousands=',')
# df['total amount'] = df['total amount'].astype(int)
# df['net return'] = df['net return'].astype(int)

clickCounter = {
    "count": 0,
    "styleA":0,
    "styleB": 0,
    "clickedA":0,
    "clickedB":0,
    "CtrA": 0, 
    "CtrB":0
}

clickCounter["count"] = 0

@app.route('/')
def home():
    global clickCounter
#     print(clickCounter)
    with open("index.html") as f:
        html = f.read()
    clickCounter["count"] = clickCounter["count"]+1
#     print("current count is "+ str(clickCounter["count"]))
    
    if(clickCounter["count"]<=10):
        if(clickCounter["count"]%2 ==0):
            # do something with A style - red
            
            html = html.replace('<a href="donate.html" target="_blank">Donate</a>',
                                '<a href="donate.html?from=A" target="_blank" style="color:red;"><b>Donate</b></a>' )
            clickCounter['styleA'] +=1
        else:
            # do something with B style - blue
            html = html.replace('<a href="donate.html" target="_blank">Donate</a>',
                                '<a href="donate.html?from=B" target="_blank" style="color:blue;"><b>Donate</b></a>' )
            clickCounter['styleB'] +=1
    #after 10 counts
    else:
        if(clickCounter['CtrA']>= clickCounter['CtrB']):
#             # do something with A style
            html = html.replace('<a href="donate.html" target="_blank">Donate</a>',
                                '<a href="donate.html?from=A" target="_blank" style="color:red;"><b>Donate</b></a>' )
            clickCounter['styleA'] +=1

        else:
#             # do something with B style
            html = html.replace('<a href="donate.html" target="_blank">Donate</a>',
                                '<a href="donate.html?from=B" target="_blank" style="color:blue;"><b>Donate</b></a>' )
            clickCounter['styleB'] +=1

    
    return html

@app.route('/browse.html')
def browse():
#     fonts: https://www.w3schools.com/cssref/tryit.asp?filename=trycss_font_timesnewroman
    df_html = df.to_html()
    return "<html>{}<html>".format("<h1>Browse</h1>"+df_html) 

# clickCounter = {
#     "count": 0,
#     "styleA":0,
#     "styleB": 0,
#     "clickedA":0,
#     "clickedB":0,
#     "CtrA": 0, 
#     "CtrB":0
# }
@app.route('/donate.html')
def donate():    
    global clickCounter

    with open("donate.html") as f:
        html = f.read()
        
    args = dict(request.args)
    if('from' in args and args['from'] == 'A'):
        clickCounter['clickedA'] +=1
        clickCounter['CtrA'] = clickCounter['clickedA']/ clickCounter['styleA']
    elif('from' in args and args['from'] == 'B'):
        clickCounter['clickedB'] +=1
        clickCounter['CtrB'] = clickCounter['clickedB']/ clickCounter['styleB']
    
#     print('clicked is', args['from'])
    return html

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
#     print("email is ", email)
    
    #if valid email
    if(re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)):
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email+"\n")

        with open("emails.txt", "r") as f: # open file in read mode to check number
            num_subscribed = len(f.readlines())            

        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    
    #if not valid email
    else:
        return jsonify("Invalid email...")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!
