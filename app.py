from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

question_bank = pd.read_excel('公寓大廈管理條例_題庫範例.xlsx').to_dict(orient='records')
leaderboard = []

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
        return redirect(url_for('result'))
    q = session['quiz'][session['index']]
    number = session['index'] + 1
    session['index'] += 1
    return render_template('question.html', question=q, number=number, time_limit=30)

@app.route('/result')
def result():
    elapsed = round(time.time() - session['start_time'])
    nickname = session['nickname']
    score = session['score']
    leaderboard.append({
        'nickname': nickname,
        'score': score,
        'time': elapsed,
        'timestamp': datetime.now()
    })
    sorted_board = sorted(leaderboard, key=lambda x: (-x['score'], x['time']))[:50]
    return render_template('result.html', nickname=nickname, score=score, time=elapsed, leaderboard=sorted_board)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_excel(file)
        global question_bank
        question_bank = df.to_dict(orient='records')
        return '題庫已更新成功'
    return render_template('admin.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
