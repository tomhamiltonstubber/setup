"""
My tool for running unittests using pytest for my Python projects. Running tests with the pytest -k argument was too
slow.

The tool uses a not very clever regex to find all tests, and runs them using the -k argument. Running an individual
test or test class is much fast here.

How to use:

To use, I recommend adding an alias for `pt=python ~/code/run_test.py` (add this file to your base code directory).
Then you can run it with:

1) an individual test: `pt test_foo`
2) a test case: `pt TestCase`
3) a test file: `pt  /home/tom/code/Project/tests/test_foo.py
4) a directory: `pt Project/main/`

The script uses the -k arg, so `pt test_foo` will run `pytest /home/tom/code/Project/tests/test_foo.py -k test_foo`. It
does this by building a `test_info.json` file in the `.data/` dir in your base code directory (make sure the .data/ dir
exists).

Other arguments:

Occasionally the building of `test_info.json` fails, use the -r argument to rebuild it from all files.

When using pytest-django, there's an option `--reuse-db` that means the database won't be recreated each time you run
tests. Since this can take a while, I assume this option is always true unless you use the `-x` argument. So, if a test
fails because of a database error of some sort, use the `-x` argument.

I don't like the traceback that pytest shows you, so I elect to include the tb=native option when running tests.
If you want to change it comment that line out I guess.

"""
import argparse
from glob import glob
from importlib.machinery import SourceFileLoader
import json
import os
import subprocess
import pytest
import re

re_def_match = re.compile('\n    def (test_.*?)\(self.*?\)\:', re.DOTALL)
re_func_match = re.compile('\n    def (test_.*?)\(.*?\)\:', re.DOTALL)
re_classes_match = re.compile(r'class .*?(?:\n{3}|\n$)', re.DOTALL)
re_cls_match = re.compile(r'class (.*?)\(')


class TestError(RuntimeError):
    pass


def _get_items(content, using_django):
    if using_django:
        classes = re_classes_match.findall(content)
        if classes and not all('Mock' in c[:50] for c in classes):
            for cls in classes:
                match = re_cls_match.search(cls)
                try:
                    cls_name = match.group(1)
                except AttributeError:
                    # No test cases here
                    pass
                else:
                    for func in re_def_match.findall(cls):
                        yield cls_name, func
    else:
        for func in re_func_match.findall(content):
            yield None, func


def _get_items_2(path):
    m = SourceFileLoader('m', path).load_module()
    for name, class_or_func in inspect.getmembers(foo):
        if inspect.isclass(class_or_func):
            for func_name in dir(class_or_func):
                if func_name.startswith('test_'):
                    yield(str(class_or_func), func_name)
        elif inspect.isfunction(class_or_func):
            yield None, str(class_or_func)


class TestRunner:
    using_django = False

    def __init__(self, reuse_db, force_rebuild, *args):
        self.extra_args = list(args)
        if 'manage.py' in os.listdir():
            self.using_django = True
            if reuse_db:
                self.extra_args.append('--reuse-db')
        self.project_dir = os.getcwd().split('/')[-1]
        self.test_info_path = f'../.data/{self.project_dir}_test_info.json'
        self.force_rebuild = force_rebuild

    def _check_update_files(self, files_info):
        """
        Checks all of the files that could have tests for changes in them
        """
        test_files = set(glob(f'./**/test_*.py', recursive=True)) - set(glob('./env*'))
        files_changed = False

        for file in test_files:
            if file.startswith('./env'):
                continue
            modified = os.stat(file).st_atime_ns
            file_info = files_info.get(file, {})
            if self.force_rebuild or file_info.get('last_edited') != modified:
                print(f'Updating file {file}')
                with open(file) as f:
                    content = f.read()
                tests = list(_get_items(content, self.using_django))
                # tests = list(_get_items_2(file))
                files_changed = True
            else:
                tests = file_info.get('tests', [])
            files_info[file] = {'last_edited': modified, 'tests': tests}
        if files_changed:
            with open(self.test_info_path, 'w+') as f:
                json.dump(files_info, f, indent=2)
        return files_info

    def find_tests(self, tests_data, test_str):
        for fp, data in tests_data.items():
            for testcase, test in data['tests']:
                if test == test_str:
                    if testcase:
                        yield f'{fp}::{testcase}::{test}'
                    else:
                        yield f'{fp}::{test}'

    def find_test_case(self, tests_data, test_str):
        for fp, data in tests_data.items():
            for testcase, test in data['tests']:
                if testcase == test_str:
                    if testcase:
                        yield f'{fp}::{testcase}::{test}'
                    else:
                        yield f'{fp}::{test}'

    def run(self, test_str):
        if self.force_rebuild:
            files_info = {}
        else:
            try:
                with open(self.test_info_path) as f:
                    files_info = json.load(f)
            except FileNotFoundError:
                files_info = {}
        tests_data = self._check_update_files(files_info)
        test_str_last_part = test_str.split('.')[-1]
        if test_str_last_part.startswith('test_'):
            test_str = test_str_last_part
        # When running tests, check for changed files and add test to dict
        if test_str.endswith('.py'):
            # Running tests for a file
            self.run_test(test_str, processes=4)
        elif test_str.endswith('/'):
            # Running tests for a path
            self.run_test(test_str, processes=8)
        elif test_str.startswith('test_') or test_str_last_part.startswith('test_'):
            # Running a single test
            tests = list(self.find_tests(tests_data, test_str))
            if not tests:
                print(f'No tests found for "{test_str}"')
            else:
                self.run_test(*tests)
        else:
            # Assuming it's a TestCase here/
            tests = list(self.find_test_case(tests_data, test_str))
            self.run_test(*tests)

    def run_test(self, *tests, processes=0):
        # Checking to see what's installed
        extra_args = ['--tb', 'native']

        installed_packages = subprocess.run([f'pip freeze'], shell=True, stdout=subprocess.PIPE).stdout.decode()
        if '--lf' in extra_args:
            processes = 0
        elif processes and 'pytest-xdist' in installed_packages:
            extra_args += ['-n', str(processes)]
        extra_args += self.extra_args
        tests = set(list(tests))
        print(f'Running tests {tests} with args {extra_args}')
        pytest.main(list(tests) + extra_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests.')
    parser.add_argument('test_case')
    parser.add_argument('-x', dest='new_db', action='store_true', default=False, help='Should use new db')
    parser.add_argument('-r', dest='force_rebuild', action='store_true', default=False, help='Force rebuild of tests file')
    parsed, extra_args = parser.parse_known_args()
    runner = TestRunner(not parsed.new_db, parsed.force_rebuild, *extra_args)
    runner.run(parsed.test_case)
