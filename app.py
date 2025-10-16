# app.py
from flask import Flask, request, jsonify
from SQL.Stock_DB import Stock_DB
from SQL.Metadata_DB import Metadata_DB  # assuming you defined a function in Fetch.py
from flask_cors import CORS
from core_py_files.help_functions import database_list
import os

app = Flask(__name__)
CORS(app) 

# Example: fetch and return live stock data
@app.route('/api/id_lst', methods=['GET'])
def get_id_list():
    metadata = Metadata_DB("metadata")
    id_list = metadata.query_rows('metadata')
    result = []
    for id in id_list:
        result.append({})
        result[-1]['code'] = id[0]
        result[-1]['name'] = id[1]
        result[-1]['price'] = id[2] if id[2] is not None else 0.0
        result[-1]['change'] = id[3] if id[3] is not None else 0.0
    return jsonify(result)

@app.route('/api/update', methods=['GET'])
def update_data():
    stock_id_list = database_list()
    from core_py_files.update import update
    num = update(stock_id_list)
    return jsonify({"updated": num})

@app.route('/api/stock_id_data', methods=['GET'])
def get_stock_id_data():
    stock_id = request.args.get('stock_id')
    order_by = request.args.get('order_by')
    limit = request.args.get('limit')
    where_column = request.args.get('where_column') 
    where_condition = request.args.get('where_condition') 
    if where_column and where_condition:
        where = {where_column: where_condition}
    else:
        where = {}
    stock = Stock_DB(stock_id)
    
    data = stock.query_rows('day', where_dict=where, order_by = order_by, limit = limit)
    data.reverse()  # Reverse the data order for charting
    categories = []
    values = []
    for row in data:
        categories.append(row[1])
        values.append([row[8], row[9], row[10], row[11]])  # open, close, high, low
    return jsonify({"categories": categories, "values": values})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)