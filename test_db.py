import sqlite3

conn = sqlite3.connect('blockchain.db')
cursor = conn.cursor()

# Verificar tabelas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', tables)

# Verificar estrutura da tabela transactions
try:
    cursor.execute("PRAGMA table_info(transactions)")
    columns = cursor.fetchall()
    print('Transaction columns:', columns)
except Exception as e:
    print('Error:', e)

conn.close()
