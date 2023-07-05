#!/usr/bin/env python3
"""
Allows you to push or pull from other peoples' branches.

Usage is like

python pull_pull_request.py <pull request id/push> <any other args>
"""
import os
import re
import sys
import requests
from requests.auth import HTTPBasicAuth

from subprocess import run, PIPE, CalledProcessError


def pull(origin, remote_branch_name, local_branch_name, *args):
    p = run(['git', 'branch'], check=True, stdout=PIPE, universal_newlines=True)
    branches = {b.strip(' *') for b in p.stdout.split('\n')}
    default_branch = re.search(r'^\*\s+(\w+)', p.stdout, flags=re.M).group(1)
    if local_branch_name in branches:
        run(['git', 'checkout', 'master'], check=True)
        run(['git', 'branch', '-D', local_branch_name], check=True)
    run(['git', 'fetch', origin, '{}:{}'.format(remote_branch_name, local_branch_name), *args], check=True)
    run(['git', 'checkout', local_branch_name], check=True)


def push(origin, remote_branch_name, local_branch_name, *args):
    run(['git', 'push', origin, '{}:{}'.format(local_branch_name, remote_branch_name), *args], check=True)


def main():
    first_arg = sys.argv[1]
    try:
        pr_id = int(first_arg)
    except ValueError:
        if sys.argv[1].lower() == 'push':
            p = run(['git', 'branch', '--show-current'], check=True, stdout=PIPE)
            pr_id = p.stdout.decode().split('-')[0]
            func = 'push'
        else:
            raise RuntimeError('This first arg should either be the PR ID (if pulling) or "push", if pushing')
    else:
        func = 'pull'

    p = run(['git', 'remote', '-v'], check=True, stdout=PIPE, universal_newlines=True)
    m = re.search(r'github.com:([\w\-]+/[\w\-]+)', p.stdout)
    assert m, 'repo and username not found in "git remote -v":' + repr(p.stdout)
    repo = m.group(1)
    auth = None
    username_token = os.getenv('GITHUB_USERNAME_TOKEN')
    if username_token:
        auth = HTTPBasicAuth(*username_token.split(':', 1))
    r = requests.get('https://api.github.com/repos/{}/pulls/{}'.format(repo, pr_id), auth=auth)
    r.raise_for_status()
    data = r.json()
    pr_number = data['number']
    print('Pull Request: \x1b[1;36m{title} #{number}\x1b[0m\n'.format(**data))
    head = data['head']
    remote_branch_name = head['ref']
    local_branch_name = '{}-{}'.format(pr_number, remote_branch_name)
    # could use head['repo']['git_url'] here
    origin = head['repo']['ssh_url']
    extra_args = sys.argv[2:]
    try:
        eval(func)(origin, remote_branch_name, local_branch_name, *extra_args)
    except CalledProcessError as e:
        print('error executing command: "{}"'.format(' '.join(e.cmd)))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
