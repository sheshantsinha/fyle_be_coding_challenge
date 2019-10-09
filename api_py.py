#!/usr/bin/python
# -*- coding: utf-8 -*-
# url http://172.105.39.232:5000/api/

from flask import Flask, request, jsonify
import psycopg2
import sys
app = Flask(__name__)

max_len = 127857
col = (
    'ifsc',
    'bank_id',
    'city',
    'state',
    'branch',
    'district',
    'address',
    )


def connect():
    connection = psycopg2.connect(user=sys.argv[1], password=sys.argv[2],
                                  host='localhost', port='5432',
                                  database=sys.argv[3])

    cursor = connection.cursor()
    return (connection, cursor)


def on_exception():
    result = {'title': 'Visit any of the two url',
              'url1': 'http://172.105.39.232:5000/api/branches/autocomplete?q=<>',
              'url2': 'http://172.105.39.232:5000/api/branches?q=<>'}
    return result


def query_auto(q, limit, offset):
    results = []
    (connection, cursor) = connect()

    postgres_insert_query = \
        'SELECT * FROM indian_banks WHERE branch ILIKE (%s) order by ifsc asc LIMIT (%s) '

    pattern = '%{}%'.format(q)
    cursor.execute(postgres_insert_query, (pattern, limit + offset))
    res = cursor.fetchall()

    cursor.close()
    connection.close()

    for row in res[offset:]:
        results.append(dict(zip(col, row)))
    return results


def search_all_query(q, limit, offset):

    results = []
    (connection, cursor) = connect()

    postgres_insert_query = \
        'SELECT * FROM indian_banks WHERE branch ILIKE (%s) or ifsc ILIKE (%s) or city ILIKE (%s) or state ILIKE (%s) or district ILIKE (%s) or address ILIKE (%s)  order by ifsc asc LIMIT (%s) '

    pattern = '%{}%'.format(q)
    temp = (
        pattern,
        pattern,
        pattern,
        pattern,
        pattern,
        pattern,
        limit + offset,
        )
    cursor.execute(postgres_insert_query, temp)
    res = cursor.fetchall()

    cursor.close()
    connection.close()

    for row in res[offset:]:
        results.append(dict(zip(col, row)))

    return results


@app.route('/api/branches/autocomplete')
def autocomplete():
    try:
        limit = int(request.args.get('limit'))
    except Exception, e:
        limit = max_len

    try:
        offset = int(request.args.get('offset'))
    except Exception, e:
        offset = 0
    query = request.args.get('q')

    if not query:
        return jsonify({'error': 'No query Found'})
    return jsonify({'branches': query_auto(query, limit, offset)})


@app.route('/api/branches')
def search_all():
    try:
        limit = int(request.args.get('limit'))
    except Exception, e:
        limit = max_len

    try:
        offset = int(request.args.get('offset'))
    except Exception, e:
        offset = 0

    query = request.args.get('q')

    if not query:
        return jsonify({'error': 'No query Found'})

    return jsonify({'branches': search_all_query(query, limit, offset)})


@app.route('/')
def landing_url():
    return jsonify(on_exception())


@app.route('/api')
def landing_url_api():
    return jsonify(on_exception())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
