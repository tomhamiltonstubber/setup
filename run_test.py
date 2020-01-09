#!/usr/bin/env python3.7
import argparse
from glob import glob
import importlib
import json
import os
import pytest
import re

re_def_match = re.compile('def (test_.*?)\(self.*?\)\:', re.DOTALL)
re_classes_match = re.compile(r'class .*?\n{3}', re.DOTALL)
re_cls_match = re.compile(r'class (.*?)\(')


class TestError(RuntimeError):
    pass


def _get_items(content):
    classes = re_classes_match.findall(content)
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


class TestRunner:
    def __init__(self, reuse_db, *args):
        self.extra_args = list(args)
        if reuse_db:
            try:
                import pytest_django
            except ImportError:
                pass
            else:
                self.extra_args.append('--reuse-db')
        self.project_dir = os.getcwd().split('/')[-1]
        self.test_info_path = f'../{self.project_dir}_test_info.json'

    def _check_update_files(self, files_info):
        """
        Checks all of the files that could have tests for changes in them
        """
        test_files = glob(f'TutorCruncher/**/test_*.py', recursive=True)
        files_changed = False

        for file in test_files:
            modified = os.stat(file).st_atime_ns
            file_info = files_info.get(file, {})
            if file_info.get('last_edited') != modified:
                print(f'Updating file {file}')
                with open(file) as f:
                    content = f.read()
                tests = list(_get_items(content))
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
                    yield f'{fp}::{testcase}::{test}'

    def run(self, test_str):
        try:
            with open(self.test_info_path) as f:
                files_info = json.load(f)
        except FileNotFoundError:
            files_info = {}
        tests_data = self._check_update_files(files_info)
        # When running tests, check for changed files and add test to dict
        if test_str.endswith('.py'):
            # Running tests for a file
            self.run_test(test_str, processes=4)
        elif test_str.endswith('/'):
            # Running tests for a path
            self.run_test(test_str, processes=8)
        elif test_str.startswith('test_'):
            # Running a single test
            tests = list(self.find_tests(tests_data, test_str))
            if not tests:
                print(f'No tests found for "{test_str}"')
            else:
                self.run_test(*tests)

    def run_test(self, *tests, processes=0):
        # Checking to see what's installed
        extra_args = [*self.extra_args]
        try:
            import xdist
        except ImportError:
            pass
        else:
            extra_args += ['-n', str(processes)]

        print(f'Running tests {tests} with args {extra_args}')
        pytest.main(list(tests) + extra_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests.')
    parser.add_argument('test_case')
    parser.add_argument('-x', dest='new_db', action='store_true', default=False, help='Should use new db')
    parsed, extra_args = parser.parse_known_args()
    runner = TestRunner(not parsed.new_db, *extra_args)
    runner.run(parsed.test_case)
