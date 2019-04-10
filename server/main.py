from flask import flask

app = Flask(__name__)

@app.route('/')
def mainPage():
	return "Welcome to aMAZE.com";

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80);
