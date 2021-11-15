from flask import Flask, render_template, request, url_for, flash, redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    contato = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(150), nullable=True)
    content = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.CHAR, default='M')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Campo de preenchimento obrigatório')
        else:
            new_post = Posts(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/valida', methods=('GET', 'POST'))
def valida():
    if request.method == 'POST':
        id = request.form['id']
        content = request.form['content']
        padrao = get_post(id)
        if not id or not content:
            flash('Campo de preenchimento obrigatório')
        else:
            if content == padrao.content:
                return redirect(url_for('escola'))
            else:
                return redirect(url_for('index'))
    return render_template('valida.html')

@app.route('/escola')
def escola():
    return render_template('escola.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        content = request.form['content']
        tipo = 'U'
        if not title or not content:
            flash('Campo de preenchimento obrigatório')
        else:
            new_user = Posts(id=id, title=title, content=content, tipo=tipo)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('outros'))
    return render_template('login.html')

@app.route('/mensagens')
def mensagens():
    posts = Posts.query.all()
    return render_template('mensagens.html', posts=posts)

@app.route('/voluntarios')
def voluntarios():
    vlt = Posts.query.all()
    return render_template('voluntarios.html', volunteer=vlt)

@app.route('/outros')
def outros():
    othr = Posts.query.all()
    return render_template('outros.html', other=othr)

@app.route('/<int:post_id>')
def post(post_id):
    pst = get_post(post_id)
    if pst.tipo == 'M':
        return render_template('post.html', postagem=pst)
    elif pst.tipo == 'V':
        return render_template('volunt.html', postagem=pst)
    else:
        return render_template('others.html', postagem=pst)

def get_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return post

@app.route('/cadastro', methods=('GET','POST'))
def cadastro():
    if request.method == 'POST':
        title = request.form['title']
        contato = request.form['contato']
        email = request.form['email']
        content = request.form['content']
        tipo = request.form['tipo']

        if not title or not content:
            flash('Campo de preenchimento obrigatório')
        else:
            new_post = Posts(title=title, contato=contato, email=email, content=content, tipo=tipo)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('voluntarios'))
    return render_template('cadastro.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    pst = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        contato = request.form['contato']
        email = request.form['email']
        content = request.form['content']
        tipo = request.form['tipo']

        if not title:
            flash('Nome é obrigatório')
        else:
            pst.title = title
            pst.contato = contato
            pst.email = email
            pst.content = content
            pst.tipo = tipo
            db.session.commit()
            return redirect(url_for('confirmacao'))
    return render_template('edit.html', edicao=pst)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    pst = get_post(id)
    db.session.delete(pst)
    db.session.commit()
    return redirect(url_for('confirmacao'))

@app.route('/confirmacao')
def confirmacao():
    return render_template('confirmacao.html')

@app.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')