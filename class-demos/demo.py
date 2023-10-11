import psycopg2


### demo 1
# # create database "example"
# connection = psycopg2.connect('dbname=example user=postgres password=Oll1N00sh1n') 

# # create interface for queuing transactions
# cursor = connection.cursor()

# # create transaction
# cursor.execute('''
#     CREATE TABLE table2 (
#         id INTEGER PRIMARY KEY,
#         completed BOOLEAN NOT NULL DEFAULT False
#     );
# ''')

# cursor.execute('INSERT INTO table2 (id, completed) VALUES (1, true);')

# # commit all transactions
# connection.commit()

# # close connection
# connection.close()
# cursor.close()

### demo 2
# # create database "example"
# connection = psycopg2.connect('dbname=example user=postgres password=Oll1N00sh1n') 

# # create interface for queuing transactions
# cursor = connection.cursor()

# # drop table2 if it exists
# cursor.execute('DROP TABLE IF EXISTS table2;')

# # create transaction
# cursor.execute('''
#     CREATE TABLE table2 (
#         id INTEGER PRIMARY KEY,
#         completed BOOLEAN NOT NULL DEFAULT False
#     );
# ''')
# # insert value via tuple
# cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

# # insert value via dictionary and naming variables
# SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'
# data = {
#     'id': 2,
#     'completed': False
#     }
# cursor.execute(SQL,data)

# # commit all transactions
# connection.commit()

# # close connection
# connection.close()
# cursor.close()

### demo 3
# create database "example"
connection = psycopg2.connect('dbname=example user=postgres password=Oll1N00sh1n') 

# create interface for queuing transactions
cursor = connection.cursor()

# drop table2 if it exists
cursor.execute('DROP TABLE IF EXISTS table2;')

# create transaction
cursor.execute('''
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
''')
# insert value via tuple
cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

# insert value via dictionary and naming variables
SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'
data = {
    'id': 2,
    'completed': False
    }
cursor.execute(SQL,data)

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'
data = {
    'id': 3,
    'completed': True
    }
cursor.execute(SQL,data)

# fetch the table results
cursor.execute('SELECT * from table2;')

# fetch all results
# result = cursor.fetchall()
# print('fetch all:', result)

# fetch many results
result = cursor.fetchmany(2)
print('fetch many(2):', result)

# fetch one result will fetch the most recent transaction
result = cursor.fetchone()
print('fetch one:', result)



# commit all transactions
connection.commit()

# close connection
connection.close()
cursor.close()