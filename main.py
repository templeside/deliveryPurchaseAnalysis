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
# print(df)
@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()
    return html

@app.route('/browse.html')
def browse():
    return df.to_html()

@app.route('/donate.html')
def donate():
    return "donate or die..."

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
