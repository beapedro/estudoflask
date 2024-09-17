from flask import Flask, render_template, request, redirect


class Jogo:
 
   def __init__(self, nome, categoria, console):
       self.nome=nome
       self.categoria=categoria
       self.console=console     
app = Flask(__name__)

jogo1= Jogo('Tetris', 'Puzzle', 'Atari')
jogo2= Jogo('Naruto', 'Lutinha', 'Ps2')
jogo3= Jogo('Lol','Moba','PC')
lista =  [jogo1,jogo2,jogo3]

@app.route('/')
def index():
   

    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
   
   nome = request.form['nome']
   categoria = request.form['categoria']
   console = request.form['console']

   jogo = Jogo(nome, categoria, console)
   lista.append(jogo)
   return redirect('/')

app.run()