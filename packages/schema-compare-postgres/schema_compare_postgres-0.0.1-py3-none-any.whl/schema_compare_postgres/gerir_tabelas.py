

def obter_tabelas(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            '''
                SELECT table_name
                FROM information_schema.tables A
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM information_schema.tables B
                    WHERE A.table_schema = B.table_schema
                    AND (
                            A.table_name ~ (B.table_name || '\d{1}a\d{1}d\d{4}') OR
                            A.table_name ~ (B.table_name || '\d{2}a\d{1}d\d{4}') OR
                            A.table_name ~ (B.table_name || '\d{1}a\d{2}d\d{4}') OR
                            A.table_name ~ (B.table_name || '\d{2}a\d{2}d\d{4}')
                        )
                )
                AND table_name NOT LIKE '%pg_%'
                AND table_schema <> 'information_schema'
            '''
        )
        tabelas = [tupla[0] for tupla in cursor.fetchall()]
    return tabelas


def obter_colunas_tabela(conn, tabela):
    with conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{tabela}'
            ORDER BY ordinal_position
        """)
        colunas = cursor.fetchall()

    return colunas
