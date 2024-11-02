import psycopg2
from dotenv import load_dotenv
import os

def insert_data(nome, whats, nota, prod, coment):
    load_dotenv()
    # Acessa as variáveis de ambiente
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    conn_info = {
            'dbname': db_name,
            'user': db_user,
            'password': db_password,
            'host': db_host,  # ou o endereço do seu servidor
            'port': '6543'        # ou a porta que seu banco de dados está usando
        }
    conn = psycopg2.connect(**conn_info)

    cursor = conn.cursor()
    query = f"""INSERT INTO cafe.nps_response (nome_cliente, whatsapp, nota, produtos_pref, comentarios)
    VALUES (%s, %s, %s, %s, %s);"""
    cursor.execute(query, (nome, whats, nota, prod, coment))

    conn.commit()
    cursor.close()
    conn.close()