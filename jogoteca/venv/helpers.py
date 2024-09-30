from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
import os
import time
def recupera_imagem(id):

   jogo = Jogos.query.filter_by(id=id).first()

 
   for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
      if f'capa{jogo.nome + str(id)}' in nome_arquivo:
         return nome_arquivo
   return 'default.jpg'         


def deleta_arquivo(id):
   arquivo = recupera_imagem(id)
   if  arquivo != 'default.jpg':
      os.remove(os.path.join(app.config['UPLOAD_PATH'],arquivo))


def recupera_pfp(nickname):

   usuario = Usuarios.query.filter_by(nickname=nickname).first()

 
   for nome_arquivo in os.listdir(app.config['PFP_PATH']):
      if f'pfp{usuario.nickname}' in nome_arquivo:
         return nome_arquivo
   return 'defaultpfp.jpg'         


def deleta_pfp(nickname):
   arquivo = recupera_pfp(nickname)
   if  arquivo != 'defaultpfp.jpg':
      os.remove(os.path.join(app.config['PFP_PATH'],arquivo))

      
      