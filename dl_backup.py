#!/usr/bin/env python3.7
import argparse
import os
import re
import subprocess
from datetime import datetime
from devtools import sformat

OPTS = {
    'AATutorCruncher': {
        'app': 'tutorcruncher',
        'db_name': 'tutorcruncher2',
        'reset_db': 'make reset-db',
    },
    'salsa-verde': {
        'app': 'salsaverde',
        'db_name': 'salsaverde',
        'reset_db': './scripts/resetdb.sh',
    },
}


def _get_id(default_id, available_ids):
    s_id = input(f'Select the ID [{default_id}]: ') or default_id
    if s_id in available_ids:
        return s_id
    else:
        print(f'Bad key: {s_id}')
        get_id()


def main(most_recent, path, app, db_name, reset_db):
    output = subprocess.run(f'heroku pg:backups -a {app}', shell=True, stdout=subprocess.PIPE)
    output = output.stdout.decode()
    lines = re.findall(r'(.*?)  (201.*?) .*?\n', output)
    data = {}
    print()
    available_ids = []
    for id, date in lines:
        available_ids.append(id)
        print(sformat(f'{id:>10}', sformat.yellow), sformat(date, sformat.green))
    print()
    default_id = lines[0][0]

    if most_recent:
        selected_id = default_id
    else:
        selected_id = _get_id(default_id, available_ids)

    file_name = f'{selected_id}-{dict(lines)[selected_id]}.dump'
    print('Download backup:', selected_id)
    subprocess.run(f'curl -o {path}/{file_name} `heroku pg:backups:url {selected_id} -a {app}` ', shell=True)
    print('Resetting DB')
    subprocess.run(reset_db, shell=True)
    print('Restoring DB')
    start = datetime.now()
    subprocess.run(f'pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -j 12 -d {db_name} {file_name}', shell=True)
    print(f'Restored DB in {(datetime.now() - start).total_seconds()} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests.')
    parser.add_argument('-mr', dest='most_recent', action='store_true', default=False, help='Download the most recent db')
    kwargs, _ = parser.parse_known_args()
    path = os.getcwd()
    opts = OPTS[path.split('/')[-1]]
    main(kwargs.most_recent, path,**opts)
