#!user/bin/env python3
# -*- coding: gbk -*-
import sqlite3

conn = sqlite3.connect('database.db')

with open('db.sql') as f:
    conn.executescript(f.read())

    cur = conn.cursor()

    cur.execute("INSERT INTO QAs (title, content) VALUES (?, ?)",
    ('学习FLASK1','跟麦叔学习第一部分')
                )

    cur.execute("INSERT INTO QAs (title, content) VALUES (?, ?)",
                ('学习FLASK2', '跟麦叔学习第二部分')
                )



conn.commit()
conn.close()