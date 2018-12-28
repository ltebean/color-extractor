from flask import Flask, request, jsonify
import extractor
app = Flask(__name__)


@app.route('/extract', methods = ['POST'])
def upload_file():
  url = request.get_json()['url']
  print(url)
  result = extractor.extract(url)
  return jsonify(result)
		
if __name__ == '__main__':
   app.run(debug = True)