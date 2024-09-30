import sqlite3, os, csv

livros = []

def procurar_banco_de_dados(nome_db):
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == nome_db:
                file_path = os.path.join(root, file)
                print(f"Banco de dados encontrado em: {file_path}")
                return file_path
    print(f"Banco de dados {nome_db} não encontrado. Será criado um novo arquivo.")
    return None

def procurar_arquivo(file_name):
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == file_name:
                file_path = os.path.join(root, file)
                print(f"Arquivo CSV encontrado em: {file_path}")
                return file_path
    print(f"Arquivo {file_name} não encontrado. Será criado um novo arquivo.")
    return None

def conectar_banco(file_path):
    if file_path:
        return sqlite3.connect(file_path)  
    else:
        return sqlite3.connect('livraria.db') 

def adicionar_livro(file_path, cursor, conexao):
    if not file_path:
        file_path = os.path.join(os.getcwd(), "livros.csv")

    titulo = input('Digite o título do livro: ')
    autor = input('Digite o autor do livro: ')
    ano_publicado = int(input('Digite o ano publicado do livro: '))
    preco = float(input('Digite o preço do livro: '))

    livro = {'titulo': titulo, 'autor': autor, 'ano_publicado': ano_publicado, 'preco': preco}
    livros.append(livro)

    write_header = not os.path.exists(file_path)

    with open(file_path, mode="a", newline="") as arquivo_csv:  
        writer = csv.writer(arquivo_csv)
        if write_header:
            writer.writerow(["id", "titulo", "autor", "ano", "preco"])
        cursor.execute('INSERT INTO livros (titulo, autor, ano_publicado, preco) VALUES (?, ?, ?, ?)', 
                       (titulo, autor, ano_publicado, preco))

    conexao.commit()
    print(' >> Livro adicionado!!!')

def atualizar_livro(cursor, conexao):
    try:
        livro_id = int(input("Digite o ID do livro que deseja atualizar: "))
        
        cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
        livro = cursor.fetchone()
        
        if livro:
            print(f"Livro encontrado: ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: R${livro[4]:.2f}")
            
            novo_titulo = input(f"Digite o novo título (atual: {livro[1]}): ").strip()
            novo_autor = input(f"Digite o novo autor (atual: {livro[2]}): ").strip()
            novo_ano = input(f"Digite o novo ano publicado (atual: {livro[3]}): ").strip()
            novo_preco = input(f"Digite o novo preço (atual: {livro[4]:.2f}): ").strip()

            novo_titulo = novo_titulo if novo_titulo else livro[1]
            novo_autor = novo_autor if novo_autor else livro[2]
            novo_ano = int(novo_ano) if novo_ano.isdigit() else livro[3]
            novo_preco = float(novo_preco) if novo_preco.replace('.', '', 1).isdigit() else livro[4]

            cursor.execute('''
                UPDATE livros 
                SET titulo = ?, autor = ?, ano_publicado = ?, preco = ?
                WHERE id = ?
            ''', (novo_titulo, novo_autor, novo_ano, novo_preco, livro_id))

            conexao.commit()
            print(f" >> Livro ID {livro_id} atualizado com sucesso!")
        else:
            print(f"Nenhum livro encontrado com o ID {livro_id}.")
    except ValueError:
        print("ID inválido ou erro na conversão. Por favor, insira um número inteiro válido.")
    except Exception as e:
        print(f"Erro ao atualizar o livro: {e}")
        
def remover_livro(cursor, conexao):
    try:
        livro_id = int(input("Digite o ID do livro que deseja remover: "))

        cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
        livro = cursor.fetchone()

        if livro:
            print(f"Livro encontrado: ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: R${livro[4]:.2f}")
            confirmacao = input("Tem certeza que deseja remover este livro? (s/n): ").strip().lower()
            
            if confirmacao == 's':
                cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
                conexao.commit()
                print(f" >> Livro ID {livro_id} removido com sucesso!")
            else:
                print(" >> Operação de remoção cancelada.")
        else:
            print(f"Nenhum livro encontrado com o ID {livro_id}.")
    except ValueError:
        print("ID inválido. Por favor, insira um número inteiro válido.")
    except Exception as e:
        print(f"Erro ao remover o livro: {e}")

def exibir_livros(cursor):
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    
    if livros:
        print(">>>Lista de Livros<<<")
        for livro in livros:
            print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: R${livro[4]:.2f}")
        print("---"*30)
    else:
        print("Nenhum livro cadastrado.")
        print("---"*30)
        
def buscar_livro(cursor):
    titulo = input("Digite o título do livro que deseja buscar: ").strip()
    
    cursor.execute("SELECT * FROM livros WHERE titulo LIKE ?", (f"%{titulo}%",))
    livros_encontrados = cursor.fetchall()
    
    if livros_encontrados:
        print(">>>Livros encontrados<<<")
        for livro in livros_encontrados:
            print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: R${livro[4]:.2f}")
            print("---"*30)
    else:
        print("Erro ao buscar livro, por favor tente novamente.")
        print("---"*30)

def exportar(file_path, cursor):
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()

    with open(file_path, 'w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(["ID", "Título", "Autor", "Ano", "Preço"])
        for livro in livros:
            escritor.writerow(livro)

    print(" >> Exportacao concluida << ")

def importar(file_path, cursor, conexao):
    with open(file_path, 'r') as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)  # Pula o cabecalho
        for linha in leitor:
            cursor.execute('INSERT INTO livros (titulo, autor, ano_publicado, preco) VALUES (?, ?, ?, ?)', 
                           (linha[1], linha[2], int(linha[3]), float(linha[4])))
        conexao.commit()
    print(" >> Importacao concluida << ")

def backup(file_path, cursor, conexao):
    print()


def main():
    nome_db = input('Digite o nome do banco de dados existente (ex: livraria.db): ')
    db_path = procurar_banco_de_dados(nome_db)
    
    conexao = conectar_banco(db_path)
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

    file_name = input('Digite o nome do arquivo CSV para salvar os livros (ex: livros.csv): ')
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
            opc = int(input('Escolha uma das opções: '))
        except ValueError:
            print('Opção inválida! Insira um número.')
            continue

        if opc == 1:
            adicionar_livro(file_path, cursor, conexao)
        elif opc == 2:
            exibir_livros(cursor)
        elif opc == 3:
            atualizar_livro(cursor, conexao)
        elif opc == 4:
            remover_livro(cursor, conexao)
        elif opc == 5:
            buscar_livro(cursor)
        elif opc == 6:
            exportar(file_path, cursor)
        elif opc == 7:
            importar(file_path, cursor, conexao)
        elif opc == 8:
            backup(file_path, cursor, conexao)
        elif opc == 0:
            print("Encerrando o programa... Obrigado pela preferência!")
            break
        else:
            print('Opção inválida, tente novamente...')

    conexao.close()

if __name__ == "__main__":
    main()