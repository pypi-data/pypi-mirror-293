import psycopg2
from .gerir_tabelas import obter_tabelas, obter_colunas_tabela
from .gerir_procedure import obter_procedures
from psycopg2.extensions import connection


def conectar(banco, user, password, host, port=5432):
    """
    Realiza conexão com banco de dados postgres

    :param banco: Banco
    :param user: Usuario
    :param password: Senha
    :param host: Servidor
    :param port: Porta, sendo padrão 5432
    :return: Conexão com banco de dados
    """

    try:
        conn = psycopg2.connect(
            dbname=banco,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except psycopg2.Error as e:
        print(e)
        conn = None
    return conn


def inserir_registro(registro):

    """
    Insere uma mensagem no arquivo de Log.

    :param registro: Mensagem a inserir no arquivo de log.
    :return:
    """

    nome_arquivo = f'compare.txt'
    try:
        # Tenta abrir o arquivo no modo leitura para verificar se ele existe
        with open(nome_arquivo, 'r'):
            pass
    except FileNotFoundError:
        # Se o arquivo não existe, cria o arquivo
        with open(nome_arquivo, 'w'):
            pass

    # Abre o arquivo no modo de escrita para adicionar o registro
    with open(nome_arquivo, 'a') as arquivo:
        arquivo.write(registro + '\n')


def verificar_conexoes(conexao_banco_origem, conexao_banco_destino):
    return isinstance(conexao_banco_origem, connection) and isinstance(conexao_banco_destino, connection)


def comparar_estruturas_tabelas(conexao_banco_origem, conexao_banco_destino):
    """
    Compara as tabelas e views dos bancos recebidos no parametro, em busca de diferenças.
    Salvando o resultado em um arquivo .txt

    :param conexao_banco_origem: Objeto de conexão de origem
    :param conexao_banco_destino: Objeto de conexão de destino
    :return:
    """

    if not verificar_conexoes(conexao_banco_origem, conexao_banco_destino):
        print("Conexões invalidas!")
        return

    banco_origem = conexao_banco_origem.get_dsn_parameters()['dbname']
    banco_destino = conexao_banco_destino.get_dsn_parameters()['dbname']

    # Busca tabelas
    tabelas_origem = obter_tabelas(conexao_banco_origem)
    tabelas_destino = obter_tabelas(conexao_banco_destino)

    # Busca diferenças e semelhanças
    tabelas_comuns = set(tabelas_origem) & set(tabelas_destino)
    tabelas_apenas_origem = set(tabelas_origem) - set(tabelas_destino)
    tabelas_apenas_destino = set(tabelas_destino) - set(tabelas_origem)

    if tabelas_apenas_origem != set():
        registro = f"Tabelas presentes apenas no {banco_origem}: {tabelas_apenas_origem}"
        inserir_registro(registro)

    if tabelas_apenas_destino != set():
        registro = f"Tabelas presentes apenas no {banco_destino}: {tabelas_apenas_destino}"
        inserir_registro(registro)

    for tabela in tabelas_comuns:
        colunas_origem = obter_colunas_tabela(conexao_banco_origem, tabela)
        colunas_destino = obter_colunas_tabela(conexao_banco_destino, tabela)

        colunas_comuns = set(colunas_origem) & set(colunas_destino)
        colunas_apenas_origem = set(colunas_origem[0]) - set(colunas_destino[0])
        colunas_apenas_destino = set(colunas_destino[0]) - set(colunas_origem[0])

        if colunas_apenas_origem != set():
            registro = f"Tabela {tabela} - Colunas presentes apenas no {banco_origem}: {colunas_apenas_origem}\n"
            inserir_registro(registro)

        if colunas_apenas_destino != set():
            registro = f"Tabela {tabela} - Colunas presentes apenas no {banco_destino}: {colunas_apenas_destino}\n"
            inserir_registro(registro)

        for coluna_origem, coluna_destino in zip(colunas_origem, colunas_destino):
            if coluna_origem != coluna_destino:
                registro = f"Tabela {tabela} - Coluna difere: {coluna_origem} vs {coluna_destino}"
                inserir_registro(registro)


def comparar_procedures(conexao_banco_origem, conexao_banco_destino):
    """
    Compara as procedures e functions dos bancos recebidos no parametro, em busca de diferenças.
    Salvando o resultado em um arquivo .txt

    :param conexao_banco_origem: Objeto de conexão de origem
    :param conexao_banco_destino: Objeto de conexão de destino
    :return:
    """

    if not verificar_conexoes(conexao_banco_origem, conexao_banco_destino):
        print("Conexões invalidas!")
        return

    procedures_banco_origem = obter_procedures(conexao_banco_origem)
    procedures_banco_destino = obter_procedures(conexao_banco_destino)

    for procedure_name in procedures_banco_origem:
        if procedure_name in procedures_banco_destino:
            if procedures_banco_origem[procedure_name] != procedures_banco_destino[procedure_name]:
                registro = f"Diferença encontrada na procedure {procedure_name}"
                inserir_registro(registro)
        else:
            registro = f"A procedure {procedure_name} está presente apenas no primeiro banco."
            inserir_registro(registro)

    for procedure_name in procedures_banco_destino:
        if procedure_name not in procedures_banco_origem:
            registro = f"A procedure {procedure_name} está presente apenas no segundo banco."
            inserir_registro(registro)


def comparar(conexao_banco_origem, conexao_banco_destino):
    """
    Compara as tabelas, views, procedures e functions dos bancos recebidos no parametro, em busca de diferenças.
    Salvando o resultado em um arquivo .txt

    :param conexao_banco_origem: Objeto de conexão de origem
    :param conexao_banco_destino: Objeto de conexão de destino
    :return:
    :return:
    """

    if not verificar_conexoes(conexao_banco_origem, conexao_banco_destino):
        print("Conexões invalidas!")
        return

    comparar_estruturas_tabelas(conexao_banco_origem, conexao_banco_destino)
    comparar_procedures(conexao_banco_origem, conexao_banco_destino)
