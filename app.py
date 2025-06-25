from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

question_bank = pd.read_excel('公寓大廈管理條例_題庫範例.xlsx').to_dict(orient='records')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    nickname = request.form.get('nickname')
    if not nickname or not nickname.isalnum():
        return render_template('index.html', error='暱稱含不雅字或特殊符號')
    session['nickname'] = nickname
    session['quiz'] = random.sample(question_bank, 40)
    session['score'] = 100
    session['index'] = 0
    session['start_time'] = time.time()
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if session['index'] >= 40:
        return "測驗結束！"
    q = session['quiz'][session['index']]
    number = session['index'] + 1
    session['index'] += 1
    return render_template('question.html', question=q, number=number, time_limit=30)

if __name__ == '__main__':
    app.run(debug=True)
