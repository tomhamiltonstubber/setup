import subprocess
import sys
import re
from devtools import sformat


def get_branch():
    print()
    current_branch = subprocess.run('git rev-parse --abbrev-ref HEAD', shell=True, stdout=subprocess.PIPE).stdout.decode().rstrip('\n')
    output = subprocess.run('git branchmin', shell=True, stdout=subprocess.PIPE)
    branch_names = {}
    for i, branch_info in enumerate(output.stdout.decode().split('\n')):
        if not branch_info:
            continue
        name, desc = branch_info.split(',', 1)
        branch_names[i] = name
        colour = sformat.blue if name == current_branch else sformat.yellow
        print(sformat(f'{i:>5}: {name:<40}', colour), sformat(f'{desc}', sformat.green))
    print()

    try:
        id = input('ID? ')
    except EOFError:
        sys.exit()
    except KeyboardInterrupt:
        return
    try:
        selected_branch = branch_names[int(id)]
    except (KeyError, ValueError):
        print('No branch with that ID')
    else:
        subprocess.run(f'git checkout {selected_branch}', shell=True)


if __name__ == '__main__':
    get_branch()
