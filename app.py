#!/usr/bin/env pyhton
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'test'

@app.route('/')
def index():
    return render_template('interactive.html')

@app.route('/test')
def inq():
    print(request.args)
    return str(request.args)
    #return 'you sent arg: %s with value %s' % ('id',request.args.get('id'))


if __name__ == "__main__":
    app.run('0.0.0.0', 9999, True)