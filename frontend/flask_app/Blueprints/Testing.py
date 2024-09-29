import pandas as pd
from flask import Blueprint, jsonify, render_template

test_bp=Blueprint("testingStuff", __name__, url_prefix="/testing")

@test_bp.route('/TestRoute')
def helloWorld():
    return jsonify({"Hello": "World"})

@test_bp.route('/multiply/<int:num1>/<int:num2>')
def multiply(num1,num2):
    return f"{num1 * num2}"