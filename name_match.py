#!/usr/bin/python
# -*- coding=utf-8 -*-
# __author__ = 'raxxar1024'
import psycopg2

USERNAME = "postgres"
PASSWORD = "123456"
HOST = "192.168.1.248"
PORT = "5432"


def name_match(db_name, tb_name, idx):
    conn = psycopg2.connect(database=db_name, user=USERNAME, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()

    sql_str = "SELECT * FROM %s;" % tb_name
    cur.execute(sql_str)
    rows = cur.fetchall()

    for i in rows:
        if i[idx] is not None and i[idx] != "":
            print i[idx]

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # name_match("gis", "planet_osm_line", 38)
    name_match("gis", "planet_osm_point", 40)
    # name_match("gis", "planet_osm_polygon", 38)
    # name_match("gis", "planet_osm_roads", 38)
