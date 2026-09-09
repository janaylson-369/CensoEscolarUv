from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return {"versao": "0.0.1"}, 200

@app.route("/health")
def health():
 return {"health":"ok"}, 200


def main(arg=[]):
  pass

if __name__ == '__main__':
  main()