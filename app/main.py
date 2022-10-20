from unicodedata import name
from flask import Flask, render_template, request, jsonify
import requests
import json
import sqlite3
import xmltodict
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


def get_db_connection():
    conn = sqlite3.connect('db/database.sqlite3')
    #conn.row_factory = sqlite3.Row
    return conn


def get_item_id_by_name(item_name):
    url = "https://www.wowhead.com/item={0}&xml".format(item_name)
    response = requests.get(url)
    result = xmltodict.parse(response.content)
    # Puede ocurrir que el item no esté en wowhead, en tal caso, se devuelve vacío.
    if "item" in result["wowhead"]:
        item_id = result["wowhead"]["item"]["@id"]
    else: 
        item_id = ""
    return item_id


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route("/class")
def get_data():
    spec = request.args.get('spec')
    url = "https://wowtbc.gg/page-data/wotlk/bis-list/{0}/page-data.json".format(spec)
    response = requests.get(url)
    result = response.json()
    bis_list = result["result"]["pageContext"]["bisList"]
    # se verifica si se cuenta con el item_id almacenado en la base de datos.
    conn = get_db_connection()
    for item in bis_list:
        if "name" in item.keys(): # hay algunos items sin nombre, son slots.
            if "T7" in item["phase"] and not "Pre-Bis" in item["phase"]: # solo se consideran los items de T7.
                item_name = item["name"]
                res = conn.execute('SELECT * FROM items WHERE item_name = ?', (item_name,)).fetchone()
                if res is None:
                    item_id = get_item_id_by_name(item_name)
                    res = conn.execute("INSERT INTO items (item_name, item_id) VALUES (?, ?)", (item_name, item_id))
                    conn.commit()

    all_items_id = conn.execute('SELECT item_id, item_name FROM items')
    items_id = {}
    for i in all_items_id.fetchall():
        items_id[i[1]] = i[0]

    conn.close()

    return  render_template('class.html', result=bis_list, spec=spec, items_id=items_id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
