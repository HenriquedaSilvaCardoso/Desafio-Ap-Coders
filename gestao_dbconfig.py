# importando as funções necessárias
from configparser import ConfigParser


# função usada para ler o arquivo config.ini e a seção mysql que contém os dados de conexão e configuração da base
def read_db_config(filename='config.ini', section='mysql'):
    parser = ConfigParser()  # instância um parser
    parser.read(filename)  # o parser lê o arquivo
    
    db = {}  # se instância um dicionário
    if parser.has_section(section):  # checa se o parser possui a seção citada como parâmetro
        items = parser.items(section)  # lista items recebe as keys e valores reconhecidos na sessão
        for item in items:  # para item em items
            db[item[0]] = item[1]  # a key recebe o valor correspondente
    else:
        raise Exception(f'{section} not found in the {filename} file')  # erro caso não haja a seção

    return db  # retorna a configuração do banco de dados
