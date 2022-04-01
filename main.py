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
#     fonts: https://www.w3schools.com/cssref/tryit.asp?filename=trycss_font_timesnewroman
    df_html = df.to_html()
    return "<html>{}<html>".format("<h1>Browse</h1>"+df_html) 

#When setting up your A/B test for the donate page, consider creating an <a> tag on your index.html. 
#In that link, you could set the href to already include one of the queries (A or B). 
#After that, you need to figure out how to swap this query back and forth when the index.html is revisited. 
#A good way to do this may be to do string manipulation on the html you read in (such as using .replace()). 

# donate_visited_counter = 0

@app.route('/donate.html')
def donate():    
#     donate_visited_counter +=1
#         if(donate_visited_counter<=10):
#             if(donate_visited_counter%2 ==0):
#                 # do something with A style
#             else:
#                 # do something with B style
#         else:
#             if(aCTR> bCTR):
#                 # do something with A style
#             else:
#                 # do something with B style

    with open("donate.html") as f:
        html = f.read()
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
