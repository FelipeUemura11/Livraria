import sqlite3, os, csv

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

def procurar_arquivo(file_name):
    # Procura um arquivo no diretório atual e seus subdiretórios.
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == file_name:
                file_path = os.path.join(root, file)
                print(f"Arquivo encontrado em: {file_path}")
                return file_path
    print(f"Arquivo {file_name} não encontrado.")
    return None

def adicionar_livro(file_path):
    titulo = input('Digite o titulo do livro: ')
    autor = input('Digite o autor do livro: ')
    ano_publicado = int(input('Digite o ano publicado do livro: '))
    preco = float(input('Digite o preço do livro: '))

    livro = {'titulo': titulo, 'autor': autor, 'ano_publicado': ano_publicado, 'preco' : preco}

    livros.append(livro)

    with open(file_path, mode="w", newline="") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["id", "titulo", "autor", "ano", "preco"])

    cursor.execute('INSERT INTO livros (titulo, autor, ano_publicado, preco) VALUES (?, ?, ?, ?)', (titulo, autor, ano_publicado, preco))

    conexao.commit()
    print(' >> Livro adicionado!!!')


def main():
    
    file_name = input('Digite o nome do arquivo que deseje salvar: ')
    file_path = procurar_arquivo(file_name)

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

        try:
            opc = int(input('Escolha uma das opcoes: '))
        except ValueError:
            print('Opcao Invalida! Insira um numero.')
            continue
        if opc == 1:
            adicionar_livro(file_path)
        elif opc == 0:
            break
        else:
            print('Opcao invalida, tente novamente...')
    
    conexao.close()

if __name__ == "__main__":
    main()
