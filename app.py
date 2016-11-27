# -*- coding: utf-8 -*-
import random

from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'
bootstrap = Bootstrap(app)


class GuessNumberForm(FlaskForm):
    number = IntegerField(u'请输入数字（0~1000）：', validators=[
        DataRequired(u'请输入一个有效的数字！'),
        NumberRange(0, 1000, u'请输入0~1000以内的数字')
    ])
    submit = SubmitField(u'提交')


@app.route('/')
def index():
    # 生成一个0~1000的随机数，存储到session变量里
    session['number'] = random.randint(0, 1000)
    session['times'] = 10
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    times = session['times']
    result = session.get('number')  # 防止KeyError
    form = GuessNumberForm()

    if form.validate_on_submit():
        if times == 1:
            flash(u'你输了(>_<)')
            return redirect(url_for('index'))  # 流程的一个端点
        times -= 1
        session['times'] = times
        answer = form.number.data
        if answer > result:
            flash(u'太大了！你还剩下%s次机会' % times)
        elif answer < result:
            flash(u'太小了！你还剩下%s次机会' % times)
        else:
            flash(u'啊哈，你赢了！V(＾－＾)V')
            return redirect(url_for('.index'))
    return render_template('guess.html', form=form)


if __name__ == '__main__':
    app.run()
