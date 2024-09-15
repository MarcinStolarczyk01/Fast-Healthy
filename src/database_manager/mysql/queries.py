from mysql import connector

# todo: replace with users credentials
db = connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='Piotrek21@',
    database='fasthealthy'
)

cursor = db.cursor()

def insert_into_recipes(name: str, procedure: str):
    cursor.execute(f'INSERT INTO recipes VALUES({name}, {procedure})')


def select_from_recipes(columns: list[str] | str = '*', order_by='name', limit=None):
    columns = str(columns).replace("'", "").replace('[', '').replace(']', '')
    cursor.execute(f'SELECT {columns}' )

