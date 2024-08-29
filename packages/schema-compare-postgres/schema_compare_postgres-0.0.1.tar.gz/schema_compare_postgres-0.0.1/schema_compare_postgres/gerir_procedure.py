
def obter_procedures(conn):
    procedures = {}
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT PR.proname, pg_get_functiondef(PR.oid)
            FROM pg_proc PR
            INNER JOIN pg_namespace NS ON PR.pronamespace = NS.oid AND (nspname LIKE '%sc_%' OR nspname = 'public')
            WHERE prorettype <> 0
            AND proname NOT LIKE '%dblink%'
            AND proname NOT LIKE '%_pg_%'
            """
        )
        for row in cursor.fetchall():
            procedures[row[0]] = row[1]
    return procedures

