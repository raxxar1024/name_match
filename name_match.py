#!/usr/bin/python
# -*- coding=utf-8 -*-
# __author__ = 'raxxar1024'
import psycopg2

USERNAME = "postgres"
PASSWORD = "123456"
HOST = "192.168.1.248"
PORT = "5432"

MATCH_LEVEL = 0.7


def find_best_match(ori_str, str_set):
    best_str = ""
    best_factor = 0.0

    for str in str_set:
        factor = float(len(ori_str))/float(len(str[1].strip()))
        if factor > MATCH_LEVEL:
            if factor > best_factor:
                best_str = str[3]
                best_factor = factor
                if factor == 1:
                    break

    return best_factor, best_str


def find_match(str, cur_b):
    str = str.replace("'", " ")
    sql_str = "SELECT * FROM %s WHERE place_name LIKE '%s';" % ("national_place_names", "%"+str+"%")
    cur_b.execute(sql_str)
    rows = cur_b.fetchall()

    best_factor, best_str = find_best_match(str, rows)

    if best_factor > MATCH_LEVEL:
        print best_factor, str, best_str
    return best_factor, best_str


def name_match(db_name, tb_name, idx):
    conn_a = psycopg2.connect(database=db_name, user=USERNAME, password=PASSWORD, host=HOST, port=PORT)
    cur_a = conn_a.cursor()

    conn_b = psycopg2.connect(database="place_names", user=USERNAME, password=PASSWORD, host=HOST, port=PORT)
    cur_b = conn_b.cursor()

    sql_str = "SELECT * FROM %s;" % tb_name
    cur_a.execute(sql_str)
    rows = cur_a.fetchall()

    for i in rows:
        if i[idx] is not None and i[idx] != "":
            # print i[idx]
            best_factor, best_str = find_match(i[idx].strip(), cur_b)
            if best_factor > MATCH_LEVEL:
                best_str = i[idx] + "(" + best_str + ")"
                update_str = "UPDATE %s SET name=%s WHERE osm_id=%s;" % (tb_name, "'"+best_str+"'", i[0])
                print update_str
                cur_a.execute(update_str)
                conn_a.commit()

    cur_b.close()
    conn_b.close()
    cur_a.close()
    conn_a.close()

if __name__ == "__main__":
    # name_match("gis", "planet_osm_line", 38)
    name_match("gis", "planet_osm_point", 40)
    # name_match("gis", "planet_osm_polygon", 38)
    # name_match("gis", "planet_osm_roads", 38)
