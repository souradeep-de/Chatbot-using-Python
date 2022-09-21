from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from location import *

app = Flask(__name__)
preps = ["in","at","from","on","near", "of","for"]
# arti = ["a","an","the"]

def check(li,preps):                                        # function for checking if any of preps's content present in incoming massage list and return it
    length1 = len(preps)
    length2 = len(li)
    for i in range(0,length1):
        for j in range(0,length2):
            if (preps[i] == li[j]):
                return preps[i]
    return 0
def Convert(li,p):                                          # function for serching the main place name
    length = len(li)
    indexx = li.index(p)
    if(indexx == (length-1)):
        return "0";
    words=[li[indexx-1],li[indexx+1]]
    return words

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    li = list(incoming_msg.split(" "))                          # making the list of incoming massage like "i am sanmay" to ["i","am","sanmay"]
    if 'hi' in incoming_msg:
        msg.body('hello')
        responded = True
    elif check(li,preps):
        prep = check(li,preps)                                  # in there prep is preps's content which is present in incoming massage's list called li
        last = Convert(li,prep)                                 # in there last is the final place
        if(last == "0"):
            msg.body('sorry! can u write the location')
        for i in range(1,5):
            msg.body(last[0])
            msg.body(nearby(last[0],last[1],i))
            if (i!=4):
                msg.body(",")  
        responded = True
    if not responded and (app.status ==500):
        msg.body('Sorry!! i can not understand, please modify and retype this last massage')
    return str(resp)
if __name__ == '__main__':
    app.run(port=4000)
    
   
   