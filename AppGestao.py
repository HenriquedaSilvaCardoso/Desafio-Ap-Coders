# importa as bibliotecas necessárias para o funcionamento
# a primeira para conectar ao mysql e detectar erros, a segunda para resgatar os dados colocados
# na função MySQLConnection, a terceira e quarta são usadas para filtrar as despesas vencidas

from mysql.connector import MySQLConnection, Error
from gestao_dbconfig import read_db_config
import datetime
from datetime import date


# função para inserir valores dentro da tabela inquilinos, adicionei uma coluna de id PRIMARY KEY em todas as tabelas
def inq_insert(nome, idade, sexo, telefone, email):
    # Aqui defino a:
    query = "INSERT INTO inquilinos VALUES(%s, %s, %s, %s, %s, NULL)"  # Query que será executada
    args = [nome, idade, sexo, telefone, email]  # Os argumentos que serão inseridos nela
    args = list(filter(''.__ne__, args))  # E uma leve filtragem para que nenhuma string vazia seja enviada

    # Uso o try para captar erros que às vezes acontecem e para que esses erros não crashem o programa
    try:
        db_config = read_db_config()  # Uso a função no arquivo gestao_dbconfig.py para
        # resgatar os dados para fazer a conexão
        db = MySQLConnection(**db_config)
        # Passo esses dados como parâmetros para firmar a conexão com o banco de dados

        cursor = db.cursor()  # Com a conexão formada é instanciado o cursor
        cursor.execute(query, args)  # E com o cursor instanciado é executada a query e são passados os args

    except Error as error:  # Esse except capta quase qualquer erro relacionado ao MySQL
        print(error)  # E retorna o erro para poder ser corrigido

    finally:
        db.commit()  # Para que os dados sejam inseridos completamente na base de dados é necessário dar commit
        cursor.close()  # Fecha o cursor
        db.close()  # Fecha a conexão com a base de dados, isso é feito toda função por motivos de segurança


# função para inserir dados na tabela unidades
def uni_insert(proprietario, condominio, endereco):
    query = "INSERT INTO unidades VALUES(NULL, %s, %s, %s)"
    args = (proprietario, condominio, endereco)
    args = list(filter(''.__ne__, args))
    try:
        db_config = read_db_config()
        db = MySQLConnection(**db_config)

        cursor = db.cursor()
        cursor.execute(query, args)

    except Error as error:
        print(error)

    finally:
        db.commit()
        cursor.close()
        db.close()


# função para inserir dados na tabela despesa, adicionei uma foreign key para fazer o filtro por unidade
def desp_insert(descricao, tipo_despesa, valor, vencimento_fatura, status_pagamento, id_uni):
    query = "INSERT INTO despesas(descricao, tipo_despesa, valor, vencimento_fatura, status_pagamento," \
            "fk_uni_id, des_id) VALUES(%s, %s, %s, %s, %s, %s, NULL)"
    args = (descricao, tipo_despesa, valor, vencimento_fatura, status_pagamento, id_uni)
    args = list(filter(''.__ne__, args))
    try:
        db_config = read_db_config()
        db = MySQLConnection(**db_config)

        cursor = db.cursor()
        cursor.execute(query, args)

    except Error as error:
        print(error)

    finally:
        db.commit()
        cursor.close()
        db.close()


# função para resgatar todos os valores de uma tabela na ordem da tabela
def table_select(tabela):
    query = "SELECT * FROM " + tabela  # query que será executada
    try:
        db_config = read_db_config()
        db = MySQLConnection(**db_config)

        cursor = db.cursor()
        cursor.execute(query)

        for row in cursor.fetchall():  # esse for resgata cada row de dentro do cursor.fetchall() que retorna a tabela
            # inteira em rows separadas
            for col in row:  # esse for resgata as colunas dentro da rows
                print(col, end=" ")  # as colunas são imprimidas em sequência na mesma linha
            print()  # quebra a linha

    except Error as error:
        print(error)

    finally:
        # Como é um query select não é necessário o commit, pois estamos resgatando algo de dentro da base de dados
        cursor.close()
        db.close()


# função usada para filtrar os valores resgatados da tabela despesa
def desp_filter(filtro):

    try:
        # caso filtro seja 1, entra no filtro por unidade
        if filtro == 1:
            # usuário informa o id da unidade
            iduni = input('Digite o id da unidade que você quer ver as despesas: ')
            # query é completado e utiliza-se a foreign key para resgatar as rows corretas
            query = "SELECT * FROM despesas WHERE fk_uni_id = " + iduni

        # caso filtro seja 2, entra no filtro por data de vencimento
        elif filtro == 2:
            query = "SELECT * FROM despesas"  # Nesse caso é necessário resgatar todas as rows da tabela e então filtrar

        db_config = read_db_config()
        db = MySQLConnection(**db_config)

        cursor = db.cursor()
        cursor.execute(query)

        # como os resultados já estão filtrados só é necessário imprimir
        if filtro == 1:
            for despesas in cursor.fetchall():
                for col in despesas:
                    print(col, end=" ")
                print()

        # no caso das despesas vencidas elas ainda precisam ser filtradas
        elif filtro == 2:
            for despesas in cursor.fetchall():
                data = list(map(int, despesas[3].split("/")))  # o quarto valor da tupla despesas é resgatada
                # (é a vencimento_fatura) e a função split é passada pra ela com o parâmetro "/" que dividirá
                # os caracteres em uma string em partes quando identificar uma barra, exemplo: 12/3/2022, ficaria
                # ('12', '3', '2022'). Após isso esse valores são mapeados como inteiros através da função map e por
                # fim, o objeto map criado pela função é traduzido em uma lista para ficar legível pelo programa

                hoje = list(map(int, str(date.today()).split("-")))  # basicamente os mesmo eventos acima, porém como
                # date.today() não retorna um string naturalmente ele precisa ser transforma em um e o parâmetro é "-"

                # se a data da despesa for anterior a data de hoje e o status de pagamento é "Não Pago"
                if datetime.date(data[2], data[1], data[0]) < datetime.date(hoje[0], hoje[1], hoje[2]) \
                        and despesas[4] == "Não Pago":
                    for col in despesas:  # imprima
                        print(col, end=" ")
                    print()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        db.close()


# função usada para atualizar a tabela despesa
def desp_update(desp_id):
    # o id da despesa é passado para mostrar os valores atuais da row
    query = "SELECT * FROM despesas WHERE des_id = " + desp_id
    try:
        db_config = read_db_config()
        db = MySQLConnection(**db_config)

        cursor = db.cursor()
        cursor.execute(query)

        # nesses fors eles são impressos
        print("Valores Atuais: ")
        for inquilino in cursor.fetchall():
            for col in inquilino:
                print(col, end=" ")
            print()

        # aqui é dada uma chance ao usuário de voltar caso não queira realmente editar nada
        choice = int(input("Você deseja, 1 - Editar alguma informação dessa despesa ou 2 - Voltar: "))
        if choice == 2:
            return

        # essa lista contém todos as colunas de uma row e no código abaixo serão organizadas de forma que
        # não seja necessário inserir todos os valores novamentes caso queira mudar somente alguns
        cols = ["descricao = %s,", "tipo_despesa = %s,", "valor = %s,", "vencimento_fatura = %s,",
                "status_pagamento = %s,", "fk_uni_id = %s"]

        # parte inicial da query que será construída ao longo da função
        query: str = "UPDATE despesas SET "

        # o usuário insere as colunas que quer alterar e separa-as por vírgula e um espaço, essa string será
        # transformada em uma lista de strings como no filtro de vencimento
        col = input("Digite a(s) coluna(s) que deseja alterar: 1 - Descrição, 2 - Tipo, 3 - Valor,"
                    " 4 - Data de Vencimento, 5 - Status do Pagamento, 6 - Unidade relacionada"
                    "\nCaso deseje alterar vários desses campos digite os números separados por vírgula\n"
                    "Exemplo: 1, 2, 3: ").split(", ")

        # retira todos os espaços que não possuem nada dentro deles na lista caso haja
        col = list(filter(''.__ne__, col))
        col = map(int, col)  # mapeia a lista em int, ou seja, transforma os valores dentro dela em inteiros
        col = list(col)  # traduz o objeto map para que seja legível pelo programa

        args = []  # define uma lista para guardar os novos valores que serão substituídos
        if not col:
            return  # caso a lista de números esteja vazia pare a função

        if 1 in col:  # todos esses são a mesma coisa, guarda o valor novo na lista e constrói mais uma parte da query
            args.append(input("Digite a nova descrição da despesa: "))  # esse muda a descrição
            query = query + cols[0]

        if 2 in col:
            args.append(input("Digite o novo tipo da despesa: "))  # esse muda o tipo
            query = query + cols[1]

        if 3 in col:
            args.append(input("Digite o novo valor da despesa: "))  # esse muda o valor
            query = query + cols[2]

        if 4 in col:
            args.append(input("Digite o nova data de vencimento **/**/**: "))  # esse muda a data
            query = query + cols[3]

        if 5 in col:
            args.append(input("Digite o novo status de pagamento: "))  # esse muda o status de pagamento
            query = query + cols[4]

        if 6 in col:
            args.append(input("Digite a nova unidade relacionada a essa despesa"))  # esse muda a unidade relacionada
            query = query + cols[5]

        query = query[:-1]  # retira o último valor da query que nesse momento é uma vírgula se tudo foi inserido
        # corretamente
        query = query + " WHERE des_id = " + id  # finaliza a query adicionando qual row será atualizada
        args = list(filter(''.__ne__, args))  # filtra espaços vazios

        cursor.execute(query, args)  # executa o query completo

    except Error:
        print('Aconteceu algum erro, tente novamente')

    finally:
        db.commit()
        cursor.close()
        db.close()


# usado para poder navegar livremente entre seções
while True:
    try:
        # Variável guarda a escolha do usuário
        choice1 = int(input("Qual seção que você quer acessar, 1 - Inquilinos, 2 - Unidades"
                            ", 3 - Despesas e 4 - Sair: "))
        # Caso a escolha do usuário não seja uma das quatro, ele precisa reescolher
        if choice1 not in [1, 2, 3, 4]:
            print("Valor inserido não compatível")
            choice1 = int(input("Qual seção que você quer acessar, 1 - Inquilinos, 2 - Unidades"
                                ", 3 - Despesas e 4 - Sair: "))

        # fecha o programa
        if choice1 == 4:
            break

        while True:
            try:
                # se a escolha for 1, o usuário vai para a seção dos inquilinos
                if choice1 == 1:
                    # Usuário escolhe o que vai fazer dentro da seção dos inquilinos
                    choice2 = int(input("O que você deseja fazer, 1 - Ver os inquilinos registrados "
                                        ", 2 - Cadastrar novos inquilinos ou 3 para voltar: "))

                    # ele pode sair
                    if choice2 == 3:
                        break

                    # exibir os valores dentro da tabela inquilinos
                    if choice2 == 1:
                        table_select("inquilinos")

                    # ou inserir novos valores dentro da tabela inquilinos
                    elif choice2 == 2:
                        inq = [input("Digite o nome do inquilino: "),
                               input("Digite a idade do inquilino: "),
                               input("Digite o sexo do inquilino (M - masculino, F - feminino, O - outro): "),
                               input("Digite o número de telefone do inquilino no padrão (**)9****-****: "),
                               input("Digite o email do inquilino: ")]

                        inq_insert(inq[0], inq[1], inq[2], inq[3], inq[4])  # os quais são passados como argumento

                # se a escolha do usuário for 2, ele vai para seção das unidades
                elif choice1 == 2:
                    # Usuário escolhe o que vai fazer dentro da seção das unidades
                    choice2 = int(input("O que você deseja fazer, 1 - Ver as unidades registrados "
                                        ", 2 - Cadastrar novas unidades ou 3 para voltar: "))

                    # ele pode sair
                    if choice2 == 3:
                        break

                    # exibir os valores dentro da tabela unidades
                    if choice2 == 1:
                        table_select("unidades")

                    # ou inserir novos valores dentro da tabela despesas
                    elif choice2 == 2:
                        uni = [input("Digite o nome do proprietário da unidade: "),
                               input("Digite o condomínio da unidade: "),
                               input("Digite o endereço da unidade: ")]

                        uni_insert(uni[0], uni[1], uni[2])  # os quais serão usados como argumentos

                # se a escolha do usuário for 3, ele vai para seção das despesas
                elif choice1 == 3:
                    # Usuário escolhe o que vai fazer dentro da seção das despesas
                    choice2 = int(input("O que você deseja fazer, 1 - Ver as despesas registradas, "
                                        "2 - Cadastrar novas despesas, 3 - Edição de despesas e 4 para voltar: "))

                    # ele pode sair
                    if choice2 == 4:
                        break

                    # exibir os valores completos da tabela despesas ou filtrá-la por unidade ou vencimento
                    if choice2 == 1:
                        choice3 = int(input("Você deseja, 1 - Exibir todos os valores da tabela despesas,"
                                            " 2 - Exibir as despesas de uma unidade específica ou"
                                            " 3 - Exibir as despesas vencidas: "))
                        if choice3 == 1:
                            table_select("despesas")

                        elif choice3 == 2:
                            desp_filter(1)

                        elif choice3 == 3:
                            desp_filter(2)

                    # inserir novos valores na tabela despesas que
                    elif choice2 == 2:
                        des = [input("Digite uma descrição breve da despesa: "),
                               input("Digite o tipo da despesa(semanal/mensal/anual): "),
                               input("Digite o valor da despesa : "),
                               input("Digite a data de vencimento, dessa forma: **/**/****: "),
                               input("Digite o status de pagamento: "),
                               input("Digite o id da unidade relacionada a essa despesa: ")]

                        desp_insert(des[0], des[1], des[2], des[3], des[4], des[5])  # serão passados como argumentos

                    # ou editar os valores de uma das rows da tabela despesas
                    elif choice2 == 3:
                        id = input("Digite o id da despesa que você deseja editar: ")
                        desp_update(id)

            except ValueError:
                print('Valor Impossível')  # usado quando não é inserido nada nas escolhas

    except Error as error:
        print(error)

    except ValueError:
        print('Valor Impossível')  # usado quando não é inserido nada nas escolhas
