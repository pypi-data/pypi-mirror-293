
# Comparador de Estruturas de Bancos de Dados PostgreSQL

Este pacote Python fornece funcionalidades para comparar as estruturas de dois bancos de dados PostgreSQL, incluindo tabelas, views, procedures e funções. O resultado da comparação é registrado em um arquivo de log para análise.

## Funcionalidades

- **Comparação de Tabelas**: Identifica diferenças entre as tabelas dos bancos de origem e destino, listando tabelas únicas em cada banco e diferenças nas colunas das tabelas comuns.
- **Comparação de Procedures e Functions**: Compara o código de procedures e functions entre os bancos, identificando diferenças ou elementos exclusivos de cada banco.

## Instalação

Para instalar o pacote, utilize:

```bash
pip install schema_compare_postgres
```

## Uso

### Conectando ao Banco de Dados

Para utilizar o pacote, primeiro, você deve se conectar aos bancos de dados de origem e destino:

```python
from schema_compare_postgres import conectar

conn_origem = conectar(banco="nome_banco_origem", user="usuario", password="senha", host="localhost")
conn_destino = conectar(banco="nome_banco_destino", user="usuario", password="senha", host="localhost")
```

### Comparando Estruturas

Depois de estabelecer a conexão, você pode realizar a comparação entre as estruturas dos dois bancos:

```python
from schema_compare_postgres import comparar

comparar(conn_origem, conn_destino)
```

Os resultados da comparação serão armazenados em um arquivo `compare.txt`, gerado na raiz do seu projeto.

### Funções Disponíveis

- `conectar(banco, user, password, host, port=5432)`: Estabelece uma conexão com um banco de dados PostgreSQL.
- `comparar(conexao_banco_origem, conexao_banco_destino)`: Compara tabelas, views, procedures e functions entre dois bancos de dados.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues no repositório.

## Licença

Este projeto está licenciado sob a licença MIT.
