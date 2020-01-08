import argparse
import sys
import re
import subprocess
from devtools import sformat


def fmt(s):
    return sformat(s, sformat.blue, sformat.bold)


def get_command(parsed):
    cmd_kwgs = {}
    if not parsed.test_case:
        print('Running all tests')
        return {'n': 8}
    if len(parsed.test_case) == 1:
        test_case = parsed.test_case[0]
        if ':' in test_case:
            test_case = re.findall(r'(.*?)\:\d', test_case)[0]
        if '/' in test_case and not test_case.endswith('.py'):
            print('Running tests for path', fmt(test_case))
            return {'test_path': test_case, 'n': 8}
        if '.py' in test_case:
            print('Running tests for file', fmt(test_case))
            return {'test_path': test_case, 'n': 8}
        elif '.' in test_case:
            test_case = test_case.split('.')[1]
            print('Running tests for test', fmt(test_case))
            return {'test_path': test_case}
        elif 'test_' in test_case:
            print('Running tests for test', fmt(test_case))
            return {'test_path': test_case}
        else:
            print('Running tests for TestCase', fmt(test_case))
            return {'test_path': test_case, 'n': 4}
    else:
        assert len(parsed.test_case) == 2
        test_path, test_case = parsed.test_case
        if ':' in test_path:
            test_path = re.findall(r'(.*?)\:\d', test_path)[0]
        if '.' in test_case and not test_case.endswith('_'):
            test_case = test_case.replace('.', '::')
            print('Running tests for test', fmt(test_case))
            return {'test_path': f'{test_path}::{test_case}'}
        elif 'test_' in test_case:
            print('Running tests for test', fmt(test_case))
            return {'test_path': test_path, 'k': test_case}
        print('Running tests for TestCase', fmt(test_case))
        return {'test_path': test_path, 'k': test_case.split(".")[0]}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests.')
    parser.add_argument('test_case', nargs='+', default=[])
    parser.add_argument('-x', dest='new_db', action='store_true', default=False, help='Should use new db')
    parsed, extra_args = parser.parse_known_args()
    if not parsed.new_db:
        extra_args.append('--reuse-db')
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    test_args = get_command(parsed)
    test_path = test_args.pop('test_path', '')
    if 'pytest-xdist' not in installed_packages:
        test_args.pop('n', None)
    if 'pytest-django' not in installed_packages:
        try:
            extra_args.remove('--reuse-db')
        except ValueError:
            pass
    test_args = ''.join(f'-{k} {v}' for k, v in test_args.items())
    subprocess.run(f'pytest {test_path} {test_args} {" ".join(extra_args)}', shell=True)
