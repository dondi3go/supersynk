from flask import Flask

app = Flask("superynk server")

@app.route('/api/toto')
def status():
  body = '{"Status":"OK"}'
  return body, 200, {'Access-Control-Allow-Origin': '*', 'Connection': 'Keep-Alive', 'Keep-Alive': 'timeout=5, max=100', 'Content-Type': 'application/json'}

if __name__ == '__main__':
  app.run(port=9999)