from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/",methods=["POST"])
def helloWorld():
  return "Hello, cross-origin-world!"

if __name__=="__main__":
	app.run()