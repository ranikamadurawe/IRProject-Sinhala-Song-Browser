from flask import Flask, render_template, redirect, url_for,request
from flask import make_response,jsonify
from preprocessing import QueryProcessor


app = Flask(__name__)
qp = QueryProcessor()

@app.route('/search_general', methods=['POST'])
def query():
   message = None
   searchQuery = request.json['searchQuery']
   result = qp.generateQuery(searchQuery)
   return jsonify(result)


@app.route('/search_faceted', methods=['POST'])
def facQuery():
   message = None
   facQuery = request.json['facQuery']
   result = qp.advancedQuery(facQuery)
   return jsonify(result)
        

if __name__ == "__main__":
    app.run(debug = True)
