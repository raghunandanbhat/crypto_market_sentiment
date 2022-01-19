from flask import Flask, render_template, request, redirect, url_for, session, jsonify, session
import pymongo
from jinja2 import Template
import datetime

app = Flask(__name__)

#connect to mongo db
try:
    client = pymongo.MongoClient("mongodb+srv://username:password@cluster0.lsras.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["crypto_mmi"]
    #mmi collection
    mmi_collection = db["mmi_by_date"]
except:
    print("Couldn't establish database connection")

@app.route("/", methods=['GET', 'POST'])
def success():
    #mmi_val = mmi_collection.find({"date":datetime.datetime.today().replace(hour=00, minute=00, second=00, microsecond=000000)})
    #dt = datetime.datetime(2021, 12, 17, 00, 00, 00)
    dt = datetime.datetime.today().replace(hour=00, minute=00, second=00, microsecond=000000)
    mmi_val = mmi_collection.find_one({"date": dt})
    total_mmi = mmi_val['overall']
    btc_mmi = mmi_val['specific'][0]['mmi']
    eth_mmi = mmi_val['specific'][1]['mmi']
    bnb_mmi = mmi_val['specific'][2]['mmi']
    doge_mmi = mmi_val['specific'][3]['mmi']
    shib_mmi = mmi_val['specific'][4]['mmi']
    return render_template('dashboard.html', total_mmi=total_mmi, btc_mmi=btc_mmi, eth_mmi=eth_mmi, bnb_mmi=bnb_mmi, doge_mmi=doge_mmi, shib_mmi=shib_mmi)


if __name__ == "__main__":
    app.run(port = 3000, debug=True)
