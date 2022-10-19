from flask import Flask, render_template, request, jsonify
import requests
import xmltodict
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


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

    return  render_template('class.html', result=bis_list, spec=spec)


@app.route("/item_id")
def get_item_id():
    item_name = request.args.get('name')
    url = "https://www.wowhead.com/item={0}&xml".format(item_name)
    response = requests.get(url)
    result = xmltodict.parse(response.content)
    item_id = result["wowhead"]["item"]["@id"]

    return jsonify({"item_id": item_id})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)



