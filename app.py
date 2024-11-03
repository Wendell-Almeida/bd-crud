from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(host='localhost', user='root', password='', database='atividade', auth_plugin='mysql_native_password')
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listagem', methods=['GET'])
def listagem():
    cursor.execute('SELECT * FROM Jogo')
    games = cursor.fetchall() 
    return render_template('index.html', games=games)

@app.route('/listagem_uniaria', methods=['POST'])
def listagem_uniaria():
    nome = request.form['nome']
    cursor.execute('SELECT * FROM Jogo WHERE nome_jogo = %s', (nome,))
    game = cursor.fetchall() 
    return render_template('index.html', game=game)

@app.route('/adicionar', methods=['GET', 'POST']) 
def inserir():
    nome = request.form['nome']
    descricao = request.form['descricao']
    nota = request.form['nota']
    tema = request.form['tema']
    genero = request.form['genero']

    cursor.execute('INSERT INTO Jogo (nome_jogo, descricao_jogo, nota_jogo, tema_jogo, genero_jogo) VALUES (%s, %s, %s, %s, %s)', 
                   (nome, descricao, nota, tema, genero))
    db.commit()

    return listagem()

@app.route('/deletar', methods=['GET', "POST"])
def deletar():
    nome = request.form['nome']
    cursor.execute('DELETE FROM Jogo WHERE nome_jogo = %s', (nome,))
    db.commit()
    return listagem() 

@app.route('/atualizar', methods=['GET','POST'])
def atualizar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    nota = request.form['nota']
    tema = request.form['tema']
    genero = request.form['genero']

    cursor.execute('UPDATE Jogo SET descricao_jogo = %s, nota_jogo = %s, tema_jogo = %s, genero_jogo = %s WHERE nome_jogo = %s', 
                   (descricao, nota, tema, genero, nome))
    db.commit()
    return listagem()

if __name__ == '__main__':
    app.run(debug=True)