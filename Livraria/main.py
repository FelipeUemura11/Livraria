import sqlite3

livros = []

conexao = sqlite3.connect('livraria.db')

cursor = conexao.cursor()

cursor.execute('''

    CREATE TABLE IF NOT EXISTS livros(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               titulo TEXT NOT NULL,
               autor TEXT NOT NULL,
               ano_publicado INTEGER,
               preco FLOAT NOT NULL
    )
''')

def adicionar_livro():
    titulo = input('Digite o titulo do livro: ')
    autor = input('Digite o autor do livro: ')
    ano_publicado = int(input('Digite o ano publicado do livro: '))
    preco = float(input('Digite o preço do livro: '))

    livro = {'titulo': titulo, 'autor': autor, 'ano_publicado': ano_publicado, 'preco' : preco}

    livros.append(livro)

    cursor.execute('INSERT INTO livros (titulo, autor, ano_publicado, preco) VALUES (?, ?, ?, ?)', (titulo, autor, ano_publicado, preco))

    conexao.commit()
    print(' >> Livro adicionado!!!')


while True:
    print(" ==== LIVRO ==== ")
    print("[1] Adicionar")
    print("[2] Exibir")
    print("[3] Atualizar")
    print("[4] Remover")
    print("[5] Buscar")
    print("[6] Exportar CSV")
    print("[7] Importar CSV")
    print("[8] Backup")
    print("[0] Sair")

    opc = int(input('Escolha uma das opcoes: '))

    if opc == 1:
        adicionar_livro()
    elif opc == 0:
        break
    else:
        print('Opcao invalida, tente novamente...')
  
conexao.close()
