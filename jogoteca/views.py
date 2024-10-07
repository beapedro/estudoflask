from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios, Amigos
import os
from helpers import recupera_imagem, deleta_arquivo, recupera_pfp, deleta_pfp
import time 
from sqlalchemy import or_
import uuid
from datetime import datetime



@app.route('/')
def index():
 
    lista = Jogos.query.order_by(Jogos.id).all()

    

    
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', next=url_for('index')))
    
 
    user = Usuarios.query.filter_by(nickname=session['usuario_logado']).first()
 
    user_pfp = recupera_pfp(user.nickname) 
 
    return render_template(
        'lista.html', 
        titulo='Jogos', 
        jogos=lista,   
        usuario=session['usuario_logado'], 
        status='active', 
        user_pfp=user_pfp,
      
        
    )

@app.route('/novo')
def novo():
   if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', next=url_for('novo'))) 
   user = Usuarios.query.filter_by(nickname=session['usuario_logado']).first()
   user_pfp = recupera_pfp(user.nickname) 
   return render_template('novo.html', titulo='Novo Jogo', usuario = session['usuario_logado'], user_pfp = user_pfp)

@app.route('/criar', methods=['POST',])
def criar():
   
   nome = request.form['nome']
   categoria = request.form['categoria']
   console = request.form['console']

   jogo = Jogos.query.filter_by(nome=nome).first()
   
   if jogo:
      flash('Jogo já existente!')
      return redirect(url_for('criar'))
   
   novo_jogo = Jogos(nome = nome, categoria = categoria, console = console)
  
   db.session.add(novo_jogo)
   db.session.commit()

   arquivo = request.files['arquivo']
   upload_path =  app.config['UPLOAD_PATH']

   timestamp = time.time()
   timestamp_string = str(timestamp)
   arquivo.save(f'{upload_path}/capa{novo_jogo.nome + str(novo_jogo.id) + timestamp_string}.jpg')
   
   user = Usuarios.query.filter_by(nickname=session['usuario_logado']).first()
   user_pfp = recupera_pfp(user.nickname) 

   return redirect(url_for('index', usuario = session['usuario_logado'], user_pfp = user_pfp))

@app.route('/deletar/<id>')
def deletar(id):
   if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', next=url_for('index'))) 

   Jogos.query.filter_by(id=id).delete()
   db.session.commit()
   flash(f'Jogo deletado com sucesso!')  
   return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
   if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', next=url_for('editar'))) 
   jogo = Jogos.query.filter_by(id=id).first()
   capa_jogo = recupera_imagem(id)
   
   user = Usuarios.query.filter_by(nickname=session['usuario_logado']).first()
   user_pfp = recupera_pfp(user.nickname) 
   return render_template('editar.html', titulo='Editar jogo', usuario = session['usuario_logado'], jogo = jogo, capa_jogo = capa_jogo, user_pfp = user_pfp )

@app.route('/atualizar', methods=['POST',])
def atualizar():

   jogo = Jogos.query.filter_by(id=request.form['id']).first()
   
   jogo.nome = request.form['nome']
   
   jogo.categoria = request.form['categoria']
   
   jogo.console = request.form['console']
   
   db.session.add(jogo)
   db.session.commit()
   
   arquivo = request.files['arquivo']
   upload_path =  app.config['UPLOAD_PATH']

   timestamp = time.time()
   
   timestamp_string = str(timestamp)

   try:
      deleta_arquivo(jogo.id)
   
   except:
      pass
   arquivo.save(f'{upload_path}/capa{jogo.nome + str(jogo.id) + timestamp_string}.jpg')
   

 
   
   return redirect(url_for('index'))

@app.route('/usuario/<nickname>')
def usuario(nickname):
   if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', next=url_for('index')))
   
   usuario = Usuarios.query.filter_by(nickname=nickname).first()
   nome = usuario.nome
   senha = usuario.senha
   user_pfp = recupera_pfp(usuario.nickname) 
   return render_template('configuracoes.html', titulo='Configurações de usuário', usuario=nickname, nome = nome, senha = senha, statusConfig='active', user_pfp = user_pfp)

@app.route('/userupdate', methods=['POST',])
def userupdate():

   user = Usuarios.query.filter_by(nickname=request.form['nickname']).first()

   nome = user.nome

   senha = user.senha

   usuario = Usuarios.query.filter_by(nickname=request.form['nickname']).first()

   usuario.nome = request.form['nome']
   
   usuario.senha = request.form['senha']
      
   if user.nome != nome or user.senha != senha:
  
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('login'))
   
   arquivo = request.files['arquivo']
   pfp_path =  app.config['PFP_PATH']

   timestamp = time.time()
   
   timestamp_string = str(timestamp)


   deleta_pfp(usuario.nickname)
   arquivo.save(f'{pfp_path}/pfp{usuario.nickname + timestamp_string}.jpg')
   

   return redirect(url_for('index'))

@app.route('/deletaruser/<nickname>')
def deletaruser(nickname):
   if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', next=url_for('index'))) 

   Usuarios.query.filter_by(nickname=nickname).delete()
   db.session.commit()
   flash('Usuário deletado com sucesso!')  
   return redirect(url_for('login'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next = next)

@app.route('/registro')
def registro():

 return render_template('registro.html', titulo = 'Cadastro de usuário ')

@app.route('/cadastro', methods=['Post',])
def cadastro():
   
   nickname = request.form['nickname']
   nome = request.form['nome']
   senha = request.form['senha']      

   usuario = Usuarios.query.filter_by(nickname=nickname).first()

   if usuario:
        flash('Usuário já cadastrado')
        return redirect(url_for('registro'))

   if nickname == 'Bento7':
    flash('Que nome cafona, escolhe um melhor ai...')
    return redirect(url_for('registro'))
 
   novo_usuario = Usuarios(nickname = nickname, nome = nome, senha = senha)
   db.session.add(novo_usuario)
   db.session.commit()
   

 
   return redirect(url_for('login'))

@app.route('/autenticar', methods=['Post',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()

    if usuario:
        if request.form['senha'] == usuario.senha:
          session['usuario_logado'] = usuario.nickname
          flash(usuario.nickname + ' logado com sucesso!')
            
          pagina = request.form['next']
       
          if not pagina or pagina == 'None':

           return redirect(url_for('index'))
     
          else:
            return redirect(pagina)
        else:
         flash('Senha incorreta')  
         return redirect(url_for('login'))

    else:
       flash("Usuário não encontrado")  
       return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado!')
    return redirect(url_for('login'))   
     
 
    # usuario = request.form['usuario']
    # senha = request.form['senha']
    # return redirect('/novo')

@app.route('/uploads/<id>')
def imagem(id):
  upload_path =  app.config['UPLOAD_PATH'] 
  try: 
   nome_arquivo = recupera_imagem(id)
   return send_from_directory('uploads', nome_arquivo)
  except:
     (os.path.join(app.config['UPLOAD_PATH'],'default.jpg'))


@app.route('/pfpuser/<nome_arquivo>')
def pfp(nome_arquivo):
   return send_from_directory('profilepics', nome_arquivo)

@app.route('/amigos/<nickname>')
def amigos(nickname):
    # Verifica se o usuário está logado
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', next=url_for('amigos')))

    # Obtém o usuário logado
    user = Usuarios.query.filter_by(nickname=session['usuario_logado']).first()
    
    if user is None:
        flash("Usuário não encontrado.")
        return redirect(url_for('login'))

    # Recupera a foto de perfil do usuário logado
    user_pfp = recupera_pfp(user.nickname)

    # Obtém a lista de amigos
    amigos = Amigos.query.filter_by(amigo2=session['usuario_logado']).all()

    # Criar uma lista para armazenar informações dos amigos e suas fotos de perfil
    amigos_info = []
    for amigo in amigos:
        # Recupera o nickname do amigo (amigo1) da lista de amigos
        user_friend = Usuarios.query.filter_by(nickname=amigo.amigo1).first()
        
        if user_friend:
            # Aqui está a chamada para recuperar a foto de perfil do amigo usando amigo1
            amigo_pfp = recupera_pfp(user_friend.nickname)  # A função é chamada aqui com amigo1
            
            amigos_info.append({
                'nickname': amigo.amigo1,
                'mensagem': amigo.mensagem,
                'pfp': amigo_pfp
            })

    return render_template(
        'amigos.html', 
        titulo='Amigos', 
        amigos=amigos_info,  # Passa a lista com informações dos amigos
        usuario=session['usuario_logado'], 
        statusAmigo='active', 
        user_pfp=user_pfp
    )


@app.route('/solicitacao', methods=['POST'])
def solicitacao():
    amigo1 = session.get('usuario_logado') 
    amigo2 = request.form['nickname']
    mensagem = request.form['mensagem']
    user = Usuarios.query.filter_by(nickname=amigo2).first()

    if amigo1 == amigo2:
        flash('Você não pode enviar uma solicitação para você mesmo. Faça amigos de verdade :(')
        return redirect(url_for('amigos', nickname=session['usuario_logado']))

    elif not user:
        flash('Usuário não encontrado.')  
        return redirect(url_for('amigos', nickname=session['usuario_logado']))  

    amigo = Amigos.query.filter_by(amigo1=amigo1, amigo2=amigo2).first()
    
    if amigo:
        flash('Um convite já foi enviado para esse usuário, aguarde.')    
        return redirect(url_for('amigos', nickname=session['usuario_logado']))

    convite = Amigos(
        amizadeid=str(uuid.uuid4()),
        amigo1=amigo1,
        amigo2=amigo2,
        confirmacao=0,
        mensagem=mensagem,
        datainicio=datetime.now()
    )

    db.session.add(convite)
    db.session.commit()

    return redirect(url_for('amigos', nickname=session['usuario_logado']))

@app.route('/aceitaconvite/<amigo1>/<amigo2>', methods=['POST'])
def aceitaconvite(amigo1, amigo2):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', next=url_for('amigos', nickname = session['usuario_logado']))) 


    convite = Amigos.query.filter_by(amigo1=amigo1, amigo2=amigo2).first()

    if convite:
        convite.solicitacao = True
        db.session.commit()
        flash('Convite aceito com sucesso!')
    else:
        flash('Convite não encontrado.')

    return redirect(url_for('amigos', nickname=session['usuario_logado']))

@app.route('/deletaconvite/<amigo1>/<amigo2>')
def deletaconvite(amigo1, amigo2):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', next=url_for('amigos', nickname = session['usuario_logado']))) 

    convite = Amigos.query.filter_by(amigo1=amigo1, amigo2=amigo2).first()

    if convite:
        db.session.delete(convite)
        db.session.commit()
        flash('Convite recusado!')  
    else:
        flash('Convite não encontrado.')

    return redirect(url_for('amigos', nickname=session['usuario_logado']))

# @app.route('/usuario/<nickname>')
# def usuario(nickname):
#    if 'usuario_logado' not in session or session['usuario_logado'] == None:
#       return redirect(url_for('login', next=url_for('index')))
   
#    usuario = Usuarios.query.filter_by(nickname=nickname).first()
#    nome = usuario.nome
#    senha = usuario.senha
#    user_pfp = recupera_pfp(usuario.nickname) 
#    return render_template('configuracoes.html', titulo='Configurações de usuário', usuario=nickname, nome = nome, senha = senha, statusConfig='active', user_pfp = user_pfp)


# @app.route('/cadastro', methods=['Post',])
# def cadastro():
   
   # nickname = request.form['nickname']
   # nome = request.form['nome']
   # senha = request.form['senha']      

   # usuario = Usuarios.query.filter_by(nickname=nickname).first()

   # if usuario:
   #      flash('Usuário já cadastrado')
   #      return redirect(url_for('registro'))

   # if nickname == 'Bento7':
   #  flash('Que nome cafona, escolhe um melhor ai...')
   #  return redirect(url_for('registro'))
 
   # novo_usuario = Usuarios(nickname = nickname, nome = nome, senha = senha)
   # db.session.add(novo_usuario)
   # db.session.commit()
   

 
   # return redirect(url_for('login'))