## @package Main entry point for Web server.
  
import datetime
from flask import Flask, render_template

## Create the App
app = Flask(__name__)

@app.route('/')
## Handle request for default page. 
def mainPage():
    now = datetime.datetime.now()
    cur_hour = now.hour
    if cur_hour < 12:
        greet = "Good Morning "
    elif cur_hour < 17:
        greet = "Good Afternoon "
    elif cur_hour < 20:
        greet = "Good Evening "
    else:
        greet = "Good Night "

    return render_template('template.html', my_time=now, my_greet=greet, my_string="Welcome to Team aMAZE!", my_title="aMAZE.com Online Book Store",\
            my_list=["Binu Jose", "Ginto George", "Nabin Thomas", "Sandeep Panakkal"])

if __name__ == '__main__':
        ## Start the http server
        app.run(host='0.0.0.0', port=80);

