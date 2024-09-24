from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar_bd():
    conn = sqlite3.connect('database.db')
    return conn

def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            tipo TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doacoes')
    doacoes = cursor.fetchall()
    conn.close()
    return render_template('index.html', doacoes=doacoes)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        tipo = request.form['tipo']
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO doacoes (nome, quantidade, tipo) VALUES (?, ?, ?)', 
                       (nome, quantidade, tipo))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doacoes WHERE id = ?', (id,))
    doacao = cursor.fetchone()
    conn.close()
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        tipo = request.form['tipo']
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE doacoes 
            SET nome = ?, quantidade = ?, tipo = ? 
            WHERE id = ?
        ''', (nome, quantidade, tipo, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('editar.html', doacao=doacao)

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM doacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
