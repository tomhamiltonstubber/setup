import re
import subprocess
from devtools import sformat

def main():
    output = subprocess.run('heroku pg:backups', shell=True, stdout=subprocess.PIPE)
    output = output.stdout.decode()
    lines = re.findall(r'(.*?)  (201.*?) .*?\n', output)
    data = {}
    print()
    for id, date in lines:
        print(sformat(f'{id:>10}', sformat.yellow), sformat(date, sformat.green))
    print()
    default_id = lines[0][0]
    selected_id = input(f'Select the ID [{default_id}]: ') or default_id
    file_name = f'{selected_id}-{dict(lines)[selected_id]}.dump'
    print('Download backup:', selected_id)
    path = './AATutorCruncher/'
    subprocess.run(f'curl -o {path}{file_name} `heroku pg:backups:url {selected_id}` ', shell=True)
    print('Restoring DB')
    subprocess.run(
        f'{path}scripts/resetdb.sh && pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d tutorcruncher2 {path}{file_name}')

if __name__ == '__main__':
	main()
