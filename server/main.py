## @package Main entry point for Web server.

from flask import Flask

## Create the App
app = Flask(__name__)

@app.route('/')
## Handle request for default page. 
def mainPage():
	return "<html> <title> aMAZE.com Online Book Store </title> <body> Welcome to aMAZE.com  </body> </html>";

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80);
