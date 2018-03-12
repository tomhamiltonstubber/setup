import subprocess
import sys
import re
from devtools import sformat


def get_branch():
    output = subprocess.run('git branchmin', shell=True, stdout=subprocess.PIPE)
    branch_names = {}
    print()
    for i, branch_info in enumerate(output.stdout.decode().split('\n')):
        if not branch_info:
            continue
        name, desc = branch_info.split(',', 1)
        branch_names[i] = name
        print(sformat(f'{i:>5}: {name:<40}', sformat.yellow), sformat(f'{desc}', sformat.green))
    print()

    try:
        id = input('ID? ')
    except EOFError:
        sys.exit() 
    try:
        selected_branch = branch_names[int(id)]
    except (KeyError, ValueError):
        print('No branch with that ID')
    else:
        subprocess.run(f'git checkout {selected_branch}', shell=True)


if __name__ == '__main__':
    get_branch()
