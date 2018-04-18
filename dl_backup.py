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
    subprocess.run(f'curl -o ./AATutorCruncher/{file_name} `heroku pg:backups:url {selected_id}` ', shell=True)

if __name__ == '__main__':
	main()
