# 과정 6 - (문제7) 나의 소소한 이야기

from flask import Flask, render_template

app = Flask(__name__)

# [보너스 과제] - Flask의 view를 이용하여 html 출력
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/now')
def now():
    return render_template('now.html')

@app.route('/parm')
def parm():
    return render_template('parm.html')

if __name__ == '__main__':
    app.run(debug=True)