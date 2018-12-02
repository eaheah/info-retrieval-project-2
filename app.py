from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
import re
from search import Search

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/search', methods=['POST'])
@cross_origin(supports_credentials=True)
def search():
    req_data = request.get_json()
    query = req_data['query']
    if query is None:
        query = ""
    query = query.lower()
    print (query)

    exception = ""
    regex = re.compile(r'not\((.*?)\)')
    if regex.search(query):
        exception = re.search(r'not\((.*?)\)',query).group(1)
    print(exception)

    phrase = re.sub(r'not\([^)]*\)', '', query)
    print(phrase)
    s = Search(phrase,exception, index='final-hopeful').search()
    return jsonify(s)
