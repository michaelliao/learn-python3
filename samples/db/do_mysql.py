#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########## prepare ##########

# install mysql-connector-python:
# pip3 install mysql-connector-python --allow-external mysql-connector-python

import mysql.connector

# change root password to yours:
conn = mysql.connector.connect(user='root', password='password', database='test')

# Apre un nuovo cursore
cursor = conn.cursor()
# Query per creare la tabella user con id chiave primaria e un nome 
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# Query per inserire un utente con id 1 e nome Michael
cursor.execute('insert into user (id, name) values (%s, %s)', ('1', 'Michael'))
# Stampa il numero di righe interessate dalla query (in questo caso 1) 
print('rowcount =', cursor.rowcount)
# Committa i cambiamenti e chiude il cursore
conn.commit()
cursor.close()

# Apre una nuova connessione
cursor = conn.cursor()
# Seleziona l'utente con id 1
cursor.execute('select * from user where id = %s', ('1',))
# Copia in values i valori ritornati, in questo esempio Michael
values = cursor.fetchall()
# Stampa i valori ritornati
print(values)
# Chiude il cursore
cursor.close()
# Chiude la connessione
conn.close()
