from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')
    
#host 要設定IP如果沒有設定就是使用127.0.0.1:5000 OR localhost:5000
#app.run(host='192.168.0.150', port=5000, debug=True)
app.run(port=5000, debug=True)