import psycopg2

database_name = "arnab"
user_name = "arnab"
password = "1181412Arnab"
host_ip = "127.0.0.1"
host_port ="5432"

my_con = psycopg2.connect(
            database = database_name,
            user = user_name,
            password = password,
            host = host_ip,
            port = host_port
)

my_con.autocommit = True
cursor = my_con.cursor()

query = "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'unified_data'"
cursor.execute(query)
exists = cursor.fetchone()
if not exists:
    cursor.execute('CREATE DATABASE unified_data')

database_name = "unified_data"
user_name = "arnab"
password = "1181412Arnab"
host_ip = "127.0.0.1"
host_port ="5432"

my_db_con = psycopg2.connect(
            database = database_name,
            user = user_name,
            password = password,
            host = host_ip,
            port = host_port
)
my_db_con.autocommit = True
cursor = my_db_con.cursor()

cursor.execute("DROP TABLE IF EXISTS flowers")
create_flower_table = """
CREATE TABLE IF NOT EXISTS flowers (
id SERIAL PRIMARY KEY,
flower_name TEXT NOT NULL,
flower_color TEXT
);
"""
cursor.execute(create_flower_table)

cursor.execute("DROP TABLE IF EXISTS users")
create_user_table = """
CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
profession TEXT,
company TEXT
);
"""
cursor.execute(create_user_table)

sample_flowers = [
    ('Rose','Red'),
    ('Sunflower','Yellow')
]
sample_users = [
    ('Arnab Samanta','Data Scientist','NVIDIA')
]


flower_insert_query = (
    """INSERT INTO flowers (flower_name, flower_color) VALUES (%s,%s)"""
)
for sample_flower in sample_flowers:
    cursor.execute(flower_insert_query, sample_flower)

user_insert_query = (
        f"INSERT INTO users (name, profession, company) VALUES (%s,%s,%s)"
    )
for sample_user in sample_users:
    
    cursor.execute(user_insert_query, sample_user)


class CustomTable:

    def __init__(self,table_name) -> None:
        self.table_name = table_name

    def insert(self,**kwargs):
        match self.table_name:
            case 'flowers':
                insert_query = (
                    f"INSERT INTO flowers (flower_name, flower_color) VALUES {kwargs['flower_name'], kwargs['flower_color']}"
                )
            case 'users':
                insert_query = (
                    f"INSERT INTO users (name, profession, company) VALUES {kwargs['name'], kwargs['profession'], kwargs['company']}"
                )
        cursor.execute(insert_query)
        count = cursor.rowcount

        return f"{count} Record inserted successfully into {self.table_name} table"
    
    def retrieve(self,**kwargs):
        if kwargs['all']:
            select_all_records = f"SELECT * FROM {self.table_name}"
            cursor.execute(select_all_records)
            records = cursor.fetchall()
            return records
        
        select_id_records = f"""SELECT * FROM {self.table_name}
                                WHERE id = {kwargs['id']}"""
        cursor.execute(select_id_records)
        records = cursor.fetchall()

        return records



    def update(self,**kwargs):
        id_ = kwargs.pop('id')
        match self.table_name:
            case 'flowers':
                update_query = (
                    f"UPDATE flowers SET flower_name = '{kwargs['flower_name']}', flower_color = '{kwargs['flower_color']}'\
                        WHERE id = {id_}"
                )
            case 'users':
                update_query = (
                    f"UPDATE users SET name = '{kwargs['name']}', profession = '{kwargs['profession']}', company = '{kwargs['company']}' WHERE id = {id_}"
                )
        
        cursor.execute(update_query)
        count = cursor.rowcount
        return f"{count} Records updated"

    def delete(self,**kwargs):
        delete_query = f"DELETE FROM {self.table_name} \
                            WHERE id = {kwargs['id']}"
        cursor.execute(delete_query)
        count = cursor.rowcount
        return f"{count} Records deleted"

    