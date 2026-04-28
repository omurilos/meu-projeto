import matplotlib.pyplot as plt
import pymysql.cursors

conexao = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="erp",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

def logarCadastrar(decisao):
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        try:
            with conexao.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM cadastros WHERE nome = %s',
                    (nome,)
                )
                usuario = cursor.fetchone()

            if usuario and senha == usuario['senha']:
                autenticado = True

                if usuario['nivel'] == 2:
                    usuarioMaster = True

                print('Login realizado com sucesso!')
            else:
                print('Nome ou senha incorretos')

        except Exception as e:
            print('Erro no banco:', e)

    elif decisao == 2:
        print('--- Cadastro ---')
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        try:
            with conexao.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM cadastros WHERE nome = %s',
                    (nome,)
                )
                usuario = cursor.fetchone()

            if usuario:
                print('Usuário já cadastrado')
            else:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO cadastros(nome, senha, nivel) VALUES (%s, %s, %s)',
                        (nome, senha, 1)
                    )
                    conexao.commit()

                print('Usuário cadastrado com sucesso')

        except Exception as e:
            print('Erro no banco:', e)

    return autenticado, usuarioMaster


def cadastrarProdutos():
    nome = input("Digite o nome do produto: ")
    ingredientes = input('Informe os ingredientes: ')
    grupo = input('Digite o grupo: ')
    
    try:
        preco = float(input('Informe o preço: '))
    except:
        print('Preço inválido')
        return

    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                'INSERT INTO produtos (nome, ingredientes, grupo, preco) VALUES (%s, %s, %s, %s)',
                (nome, ingredientes, grupo, preco)
            )
            conexao.commit()

        print('Produto cadastrado com sucesso')

    except Exception as e:
        print('Erro ao inserir produto:', e)


def listarProduto():
    try:
        with conexao.cursor() as cursor:
            cursor.execute('SELECT * FROM produtos')
            produtos = cursor.fetchall()

    except Exception as e:
        print('Erro ao buscar produtos:', e)
        return

    if len(produtos) == 0:
        print('Nenhum produto encontrado')
        return

    print('\n--- LISTA DE PRODUTOS ---')
    for produto in produtos:
        print(f"ID: {produto['id']} | Nome: {produto['nome']} | Preço: {produto['preco']}")


def excluirProdutos():
    try:
        idDeletar = int(input('Digite o ID do produto que deseja deletar: '))
    except:
        print('ID inválido')
        return

    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                'DELETE FROM produtos WHERE id = %s',
                (idDeletar,)
            )
            conexao.commit()

        print('Produto excluído com sucesso')

    except Exception as e:
        print('Erro ao excluir produto:', e)

def listarPedidos():
    pedidos = []
    decision = 0

    while decision !=2:
        pedidos.clear()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM pedidos')
                listarPedidos = cursor.fetchall()
        except:
            print('erro no banco de dados')

        for i in listarPedidos:
            pedidos.apppend(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('nemhum pedido foi feito')

        decision = int(input('digite 1 para dar un produto com entregue e 2 para voltar'))
        if decision ==1 :
            idDeletar = int(input('digite o id do pedido entregue'))

def gerarEstatisticas():
    nomeProdutos = []
    valores = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except Exception as e:
        print('erro ao se conectar ao banco de dados: ', e)

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticasVendidos')
            vendidos = cursor.fetchall()
    except Exception as e:
        print('erro ao se conectar ao banco de dados: ', e)

    estado = int(input('digite ) para sair, 1 para pesquisar por nome e 2 para pesquisar por grupo'))

    if estado ==1:
        decisao3 = int(input("digite 1 para pesquisar por dinheiro e dois para pesquisar por grupo"))
        
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []

            for nome in range(0, len(nomeProdutos)):
                somaValor = 0
                for v in vendidos:
                    if v['nome'] == nome:
                        somaValor += v['preco']
                valores.append(somaValor)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('quantidade vendida em reais')
            plt.xlabel('produtos')
            plt.show()
        if decisao3 ==2:
                grupoUnico = []
                grupoUnico.clear()

                try:
                    with conexao.cursor() as cursor:
                        cursor.execute('select * from produtos')
                        grupo = cursor.fetchall()
                except:
                    print('erro na consulta')

                try:
                   with conexao.cursor() as cursor:
                       cursor.execute('select * from estatisticasVendidos')
                       vendidoGrupo = cursor.fetchall()
                except:
                    print('erro na consulta')

                for i in grupo:
                    grupoUnico.append(i['grupo'])

                grupoUnico = sorted(set(grupoUnico))

                qntFinal = []
                qntFinal.clear()

                for h in range(0, len(grupoUnico)):
                    qntUnitaria = 0
                    for i in vendidoGrupo:
                        if grupoUnico[h] == i['grupo']:
                            qntUnitaria += 1
                    qntFinal.append(qntUnitaria)

                plt.plot(grupoUnico, qntFinal)
                plt.ylabel('quantidade unitaria vendida')
                plt.xlabel('produto')
                plt.show()

                         





         



# ---------------- MAIN ----------------

autenticado = False
usuarioSupremo = False

while not autenticado:
    try:
        decisao = int(input('Digite 1 para logar ou 2 para cadastrar: '))
    except:
        print('Digite apenas números!')
        continue

    if decisao not in [1, 2]:
        print('Opção inválida!')
        continue

    autenticado, usuarioSupremo = logarCadastrar(decisao)


print('\nSistema iniciado!')

while True:
    print('\n--- MENU ---')
    print('1 - Cadastrar produto')
    print('2 - Listar produtos')
    print('3 - Excluir produto')
    print('4 - Listar pedidos')
    print('5 - para gerar as estatisticas')
    print('0 - Sair')

    try:
        opcao = int(input('Escolha uma opção: '))
    except:
        print('Digite apenas números')
        continue

    if opcao == 0:
        print('Saindo do sistema...')
        break

    elif opcao == 1:
        if usuarioSupremo:
            cadastrarProdutos()
        else:
            print('Apenas administradores podem cadastrar produtos')

    elif opcao == 2:
        listarProduto()

    elif opcao == 3:
        if usuarioSupremo:
            excluirProdutos()
    elif opcao ==4:
       decision = int(input('digite 1 para dar un produto com entregue e 2 para voltar'))
       if decision ==1 :
            idDeletar = int(input('digite o id do pedido entregue'))
            try:
                with conexao.cursor() as cursor:
                      cursor.execute('delete from pedidos where id = {}', format(idDeletar))
            except:
                print('erro ao dar produto como entregue')
    elif opcao == 5:
        gerarEstatisticas()
    else: 
        print('Apenas administradores podem excluir produtos')
    
        


        