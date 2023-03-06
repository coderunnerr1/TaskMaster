from flask import render_template, request, redirect, session, flash, url_for
from TaskMaster import app, db
from models import Tarefas, Usuarios

@app.route('/')
def index():
    lista = Tarefas.query.order_by(Tarefas.id)
    return render_template('lista.html', titulo='Task', tarefas=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Nova Tarefa')

@app.route('/criar', methods=['POST',])
def criar():
    tarefa = request.form['tarefa']
    descricao = request.form['descricao']
    prazo = request.form['prazo']
    status = request.form['status']
    
    tarefa_existente = Tarefas.query.filter_by(tarefa=tarefa).first()
    if tarefa_existente:
        flash('Tarefa já existente!')
        return redirect(url_for('index'))
    
    if tarefa.strip() == "":
        flash('Tarefa não pode ser vazia!')
        return redirect(url_for('index'))
    
    nova_tarefa = Tarefas(tarefa=tarefa, descricao=descricao, prazo=prazo, status=status)
    db.session.add(nova_tarefa)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    tarefa = Tarefas.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Tarefa', tarefa=tarefa)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    tarefa = Tarefas.query.filter_by(id=request.form['id']).first()
    tarefa.tarefa = request.form['tarefa']
    tarefa.descricao = request.form['descricao']
    tarefa.prazo = request.form['prazo']
    tarefa.status = request.form['status']
    
    db.session.add(tarefa)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Tarefas.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Tarefa deletada com sucesso!")
    
    return redirect(url_for('index'))
    

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = url_for('index')
    return render_template('login.html',proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' Logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash("Usuário inválido")
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))