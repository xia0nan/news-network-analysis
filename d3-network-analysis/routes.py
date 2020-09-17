import json

import numpy as np
import pandas as pd
from flask import Flask, render_template, redirect, request, jsonify, Response
import time

app = Flask(__name__)

import sys, os
PATH_PROJECT = os.path.dirname(sys.path[0])
sys.path.append(PATH_PROJECT)
PATH_PROJECT = f"{PATH_PROJECT}/"


def get_network_data():
    nodes = pd.read_csv(f'./static/data/banking_nodes.csv')
    links = pd.read_csv(f'./static/data/banking_links.csv')

    nodes = json.dumps(nodes.to_dict(orient='records'))
    links = json.dumps(links.to_dict(orient='records'))

    data = {'nodes': nodes,
            'links': links}
    return data


@app.route('/', methods=['GET'])
def network():
    data = get_network_data()
    return render_template("network.html", data=data)


if __name__ == '__main__':
    app.run(threaded=True)