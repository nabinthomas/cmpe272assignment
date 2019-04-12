## @package Main entry point for Web server.

from flask import Flask

## Create the App
app = Flask(__name__)

@app.route('/')
## Handle request for default page. 
def mainPage():
	return "Welcome to aMAZE.com";

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80);
