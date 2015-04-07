from __future__ import print_function

from contextlib import contextmanager
from string import ascii_lowercase
from random import choice
from time import time, sleep
import itertools

from cassandra.cluster import Cluster
from cassandra.query import tuple_factory


def main():
    ks = ''.join(choice(ascii_lowercase) for _ in range(5))

    with get_session() as session:
        # TODO: couldn't find a way to create a keyspace with a prepared statement
        create_ks = ("CREATE KEYSPACE " + ks +
                     " WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
        print(create_ks)
        session.execute(create_ks)
        session.set_keyspace(ks)
        
        session.execute('CREATE TABLE test (foo int PRIMARY KEY, bar int);')

        insert_for_seconds(session)
        result = get_from_test(session)
        fst, snd = lambda x: x[0], lambda x: x[1]
        print(sorted(result))
        print('values are in writetime order:',
              sorted(result, key=fst) == sorted(result, key=snd))


def insert_for_seconds(session, seconds=30):
    start_time = time()

    simple_insert = session.prepare('INSERT INTO test (foo, bar) VALUES (?, ?);')

    for i in itertools.count():
        if time() - start_time > seconds:
            break
        session.execute(simple_insert, [i, i])
        sleep(0.05)
        if i % 10 == 0:
            print('.', end='')
    print()


def get_from_test(session):
    session.row_factory = tuple_factory
    return session.execute("SELECT bar, WRITETIME(bar) FROM test;")


@contextmanager
def get_session(keyspace=None):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect(keyspace)

    yield session

    session.cluster.shutdown()
    session.shutdown()

main()
