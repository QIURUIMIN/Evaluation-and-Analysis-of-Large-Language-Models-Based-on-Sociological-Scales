#!user/bin/env python3
# -*- coding: gbk -*-
import sqlite3

conn = sqlite3.connect('database.db')

with open('db.sql') as f:
    conn.executescript(f.read())

    cur = conn.cursor()

    cur.execute("INSERT INTO QAs (title, content) VALUES (?, ?)",
    ('ѧϰFLASK1','������ѧϰ��һ����')
                )

    cur.execute("INSERT INTO QAs (title, content) VALUES (?, ?)",
                ('ѧϰFLASK2', '������ѧϰ�ڶ�����')
                )



conn.commit()
conn.close()