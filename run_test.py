import argparse
import sys
import re
import subprocess
from devtools import sformat


def fmt(s):
    return sformat(s, sformat.blue, sformat.bold)


def get_command(parsed):
    if not parsed.test_case:
        print('Running all tests')
        return 'pytest -n 8'
    if len(parsed.test_case) == 1:
        test_case = parsed.test_case[0]
        if '/' in test_case and not test_case.endswith('.py'):
            print('Running tests for path', fmt(test_case))
            return f'pytest {test_case} -n 8'
        if '.py' in test_case:
            print('Running tests for file', fmt(test_case))
            return f'pytest {test_case} -n 8'
        elif '.' in test_case:
            test_case = test_case.split('.')[1]
            print('Running tests for test', fmt(test_case))
            return f'pytest -k {test_case}'
        elif 'test_' in test_case:
            print('Running tests for test', fmt(test_case))
            return f'pytest -k {test_case}'
        else:
            print('Running tests for TestCase', fmt(test_case))
            return f'pytest -k {test_case} -n 4'
    else:
        assert len(parsed.test_case) == 2
        file_path, test_case = parsed.test_case
        if ':' in file_path:
            file_path = re.findall(r'(.*?)\:\d', file_path)[0]
        if '.' in test_case and not test_case.endswith('_'):
            test_case = test_case.replace('.', '::')
            print('Running tests for test', fmt(test_case))
            return f'pytest {file_path}::{test_case}'
        elif 'test_' in test_case:
            print('Running tests for test', fmt(test_case))
            return f'pytest {file_path} -k {test_case}'
        print('Running tests for TestCase', fmt(test_case))
        return f'pytest {file_path} -k {test_case.split(".")[0]}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests.')
    parser.add_argument('test_case', nargs='+', default=[])
    parser.add_argument('-x', dest='new_db', action='store_true', default=False, help='Should use new db')
    parsed, extra_args = parser.parse_known_args()
    if not parsed.new_db:
        extra_args.append('--reuse-db')
    subprocess.run(f'{get_command(parsed)} {" ".join(extra_args)}', shell=True)
