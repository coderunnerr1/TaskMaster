import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `TaskMaster`;")

cursor.execute("CREATE DATABASE `TaskMaster`;")

cursor.execute("USE `taskmaster`;")

# criando tabelas
TABLES = {}
TABLES['Tarefas'] = ('''
      CREATE TABLE `tarefas` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `tarefa` varchar(100) NOT NULL,
      `descricao` varchar(500) NOT NULL,
      `prazo` varchar(15) NOT NULL,
      `status` varchar (20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Bruno Divino", "BD", "alohomora"),
      ("Camila Ferreira", "Mila", "paozinho"),
      ("Guilherme Louro", "Cake", "python_eh_vida")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from taskmaster.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo as tarefas
tarefas_sql = 'INSERT INTO tarefas (tarefa,descricao, prazo, status) VALUES (%s, %s, %s, %s)'
tarefas = [
    ('Trabalho Etica','Trabalho em dupla','31/03/2023','Alto'),
    ('Baixa de xml','Baixas da mensal - fev','31/03/2023','Normal'),
    ('Aprender Java','Curso Alura','31/12/2023','Urgente')
]
cursor.executemany(tarefas_sql, tarefas)

cursor.execute('select * from taskmaster.tarefas')
print(' -------------  Tarefas:  -------------')
for tarefa in cursor.fetchall():
    print(tarefa[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()