import argparse
from datetime import datetime
from glob import glob
import json
import os
import subprocess

from flake8.api import legacy as flake8
import black
import configparser


project_checks = {
    'TutorCruncher2': ['TutorCruncher/'],
    'ventilator': ['src/', 'tests/'],
    'find-a-tutor': ['tcfat/', 'tests/'],
    'tc-virus-checker': ['tc_av/', 'tests/'],
    'SalsaVerde': ['SalsaVerde/'],
    'TCIntercom': ['tcintercom/', 'tests/'],
    'dundjeon-finder': ['DungeonFinder/'],
    'sunshine-packages': ['SunshinePackages/'],
    'TCHubspot': ['tc_hs/', 'tests/'],
    'morpheus': ['src/', 'tests/'],
    'main-platform': ['src/', 'tests/'],
}


class Linter:
    def __init__(self, force_rebuild, *args):
        self.extra_args = list(args)
        self.project_dir = os.getcwd().split('/')[-1]
        self.linter_info_path = f'../.data/{self.project_dir}_linter_info.json'
        self.force_rebuild = force_rebuild
        config = configparser.ConfigParser()
        config.read('setup.cfg')
        self.f8_config = dict(dict(config).get('flake8', {}))
        if self.f8_config:
            self.f8_config['ignore'] = ['E402'] + self.f8_config['ignore'].split(', ')
            self.f8_config['exclude'] = [i for i in self.f8_config.get('exclude', '').replace('\n', ',').split(',') if i]
        self.now = datetime.now().timestamp()

    def _check_update_files(self, files_info):
        """
        Checks all the files to see if they have been linted since they were last modified
        """
        test_files = set(glob(f'./**/**.py', recursive=True))
        files_to_check = []

        for file in test_files:
            if file.startswith('./env'):
                continue
            modified = os.stat(file).st_ctime
            file_info = files_info.get(file, {})
            if self.force_rebuild or file_info.get('last_passed', 0) <= modified:
                print(f'Linting file {file}')
                files_to_check.append(file)

        return files_to_check

    def run(self):
        if self.force_rebuild:
            files_info = {}
        else:
            try:
                with open(self.linter_info_path) as f:
                    files_info = json.load(f)
            except FileNotFoundError:
                files_info = {}
        style_guide = flake8.get_style_guide(**self.f8_config)
        files_to_check = self._check_update_files(files_info)
        print('Checking for debug...')
        debug_files = []
        for file in files_to_check:
            with open(file) as f:
                if '    debug(' in f.read():
                    debug_files.append(file)
        if debug_files:
            print('😴 Debug found in the following files:\n  ' + '\n     '.join(debug_files))
            return
        p_dirs = ' '.join(project_checks[self.project_dir])
        subprocess.run([f'black -S -l 120 --target-version py38 {" ".join(files_to_check)}'], shell=True)
        subprocess.run([f'isort {" ".join(files_to_check)}'], shell=True)
        if files_to_check:
            report = style_guide.check_files(files_to_check)
            wrong_files = [e.filename for e in report._stats._store.keys()]
            if not wrong_files:
                print('All passed')
            for file in files_to_check:
                if file in wrong_files:
                    continue
                files_info[file] = {'last_passed': self.now}
            with open(self.linter_info_path, 'w+') as f:
                json.dump(files_info, f, indent=2)
        else:
            print('No files to check')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run linter with flake8.')
    parser.add_argument('-r', dest='force_rebuild', action='store_true', default=False, help='Force rebuild of flake8 info file')
    parsed, extra_args = parser.parse_known_args()
    runner = Linter(parsed.force_rebuild, *extra_args)
    runner.run()
