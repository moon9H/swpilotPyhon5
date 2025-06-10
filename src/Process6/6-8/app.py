# 과정 6 - (문제8) 응원메세지 담아보기

import csv
from flask import Flask, render_template, request, redirect
from datetime import datetime
import html

app = Flask(__name__)

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

@app.route('/guestboard', methods=['GET', 'POST'])
def guestboard():
    if request.method == 'POST':
        # [보너스 과제] - HTML을 사용하려는 경우 escape
        name = html.escape(request.form['name'])
        content = html.escape(request.form['content'])
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # CSV 파일에 내용 추가
        with open('guestboard.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([time, name, content])

        return redirect('/guestboard')

    # CSV 파일에서 내용 읽기
    entries = []
    try:
        with open('src/Process6/6-8/guestboard.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            entries = [{'time': row[0], 'name': row[1], 'content': row[2]} for row in reader]
    except FileNotFoundError:
        pass

    # 상위 10개 내용만 표시
    entries = entries[-10:]

    return render_template('guestboard.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
