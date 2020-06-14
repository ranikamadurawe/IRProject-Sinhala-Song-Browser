from flask import Flask, render_template, redirect, url_for,request
from flask import make_response,jsonify
from preprocessing import QueryProcessor
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
qp = QueryProcessor()

@app.route('/search_general', methods=['POST'])
def query():
   message = None
   searchQuery = request.json['searchQuery']
   result = qp.generateQuery(searchQuery)
   response = jsonify(result)
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response


@app.route('/search_faceted', methods=['POST'])
def facQuery():
   message = None
   facQuery = request.json['facQuery']
   result = qp.advancedQuery(facQuery)
   response = jsonify(result)
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response
        

if __name__ == "__main__":
    app.run(debug = True)
    

