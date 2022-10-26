#!/usr/bin/env python3
import argparse
import glob
import os
import re
import subprocess
from datetime import datetime
from devtools import sformat

from operator import itemgetter

OPTS = {
    'TutorCruncher2': {
        'app': 'tutorcruncher',
        'db_name': 'tutorcruncher2',
        'reset_db': 'make reset-db',
    },
    'SalsaVerde': {
        'app': 'salsaverde',
        'db_name': 'salsaverde',
        'reset_db': './scripts/resetdb.sh',
    },
    'blog.brookehouse.com': {
        'app': 'brooke-house-blog',
        'db_name': 'brookehouseblog',
        'reset_db': './scripts/resetdb.sh',
    },
    'sunshine-packages': {
        'app': 'sunshine-packages',
        'db_name': 'sunshine',
        'reset_db': './scripts/resetdb.sh',
    },
    'hermes': {
        'app': 'tc-hermes',
        'db_name': 'tchubspot',
        'reset_db': 'make reset-db',
    },
}


def _get_id(default_id, available_ids):
    s_id = input(f'Select the ID [{default_id}]: ') or default_id
    if s_id in available_ids:
        return s_id
    else:
        print(f'Bad key: {s_id}')
        _get_id(default_id, available_ids)


def main(db_id, dont_upload, path, app, db_name, reset_db):
    output = subprocess.run(f'heroku pg:backups -a {app}', shell=True, stdout=subprocess.PIPE)
    output = output.stdout.decode()
    lines = set(re.findall(r'(.*?)  ((?:202|201).*?) .*?\n', output))
    print()

    available_ids = []
    for file in glob.glob('*.dump'):
        if file == 'latest.dump':
            continue
        id, date = file.split('-', 1)
        available_ids.append(id)
        iden = (id, date.replace('.dump', ''))
        if iden in lines:
            lines.remove(iden)
        lines.add((id, date.replace('.dump', '') + ' (local)'))

    lines = sorted(list(lines), key=itemgetter(1), reverse=True)
    for id, date in lines:
        available_ids.append(id)
        print(sformat(f'{id:>10}', sformat.yellow), sformat(date, sformat.green))
    print()
    default_id = lines[0][0]

    if db_id:
        selected_id = db_id
    else:
        selected_id = _get_id(default_id, available_ids)

    file_name = f'{selected_id}-{dict(lines)[selected_id].replace(" (local)", "")}.dump'
    full_path = f'{path}/{file_name}'
    if os.path.exists(full_path):
        print('Not downloading new db as already exists')
    else:
        print('Download backup:', selected_id)
        subprocess.run(f'heroku pg:backups:download {selected_id} -a {app} -o {full_path}', shell=True)

    print('Resetting DB')
    subprocess.run(reset_db, shell=True)
    print('Restoring DB')
    start = datetime.now()
    subprocess.run(f'pg_restore --clean --no-acl --no-owner -h localhost -U postgres -d {db_name} {file_name} -j12', shell=True)
    print(f'Restored DB in {(datetime.now() - start).total_seconds()} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests.')
    parser.add_argument('-db', default='', type=str, help='The ID of the db you want to download (eg. a1234)')
    kwargs, _ = parser.parse_known_args()
    path = os.getcwd()
    opts = OPTS[path.split('/')[-1]]
    main(kwargs.db, True, path,**opts)
