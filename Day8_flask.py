import os
from flask import Flask, render_template, request, redirect

from Day8_supportingFunctions import plot_stock_data

app = Flask(__name__)


app.vars = {'ticker' : 'AAPL',
            'open'   : False,
            'close'  : True}

@app.route("/index", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('fallOn.html')
    else:
        app.vars['ticker'] = request.form['ticker']
        app.vars['close']  = request.form['open']
        app.vars['open']   = request.form['close']
        return redirect('/chart')

@app.route("/chart")
def chart():
    print(app.vars['ticker'])
    script, div = plot_stock_data(app.vars['ticker'], app.vars['open'], app.vars['close'])
    return render_template('graph.html', script=script, div=div)

    
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = '127.0.0.1' if port == 5000 else '0.0.0.0'
    app.run(host=host, port=port, debug = (port == 5000))