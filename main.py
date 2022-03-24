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
# df = pd.read_csv("main.csv")

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()
    return html

@app.route('/browse.html')
def browse():
    return "This isn't finished dumbass..."

@app.route('/donate.html')
def donate():
    return "donate or die..."

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"(string1)@(string2).(2+characters)", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email+"\n")
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify(
    message = "Invalid email...")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!
