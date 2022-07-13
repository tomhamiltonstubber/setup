#!/usr/bin/env python3
"""
pull from and pushing to other people's pull requests

(might require an auth key for private repos)
"""
import os
import re
import sys
import requests
from requests.auth import HTTPBasicAuth

from subprocess import run, PIPE, CalledProcessError


def pull(origin, remote_branch_name, local_branch_name):
    p = run(['git', 'branch'], check=True, stdout=PIPE, universal_newlines=True)
    branches = {b.strip(' *') for b in p.stdout.split('\n')}
    default_branch = re.search(r'^\*\s+(\w+)', p.stdout, flags=re.M).group(1)
    if local_branch_name in branches:
        run(['git', 'checkout', default_branch], check=True)
        run(['git', 'branch', '-D', local_branch_name], check=True)
    run(['git', 'fetch', origin, '{}:{}'.format(remote_branch_name, local_branch_name)], check=True)
    run(['git', 'checkout', local_branch_name], check=True)


def push(origin, remote_branch_name, local_branch_name):
    run(['git', 'push', origin, '{}:{}'.format(local_branch_name, remote_branch_name)], check=True)


def main():
    if not 2 <= len(sys.argv) <= 3:
        print('usage: git ppr <pull request id> [pull/push]')
        return 1

    pr_id = int(sys.argv[1])
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
    print('Pull Request: \x1b[1;36m{title} #{number}\x1b[0m\n'.format(**data))
    head = data['head']
    remote_branch_name = head['ref']
    local_branch_name = '{}-{}'.format(head['user']['login'], remote_branch_name)
    # could use head['repo']['git_url'] here
    origin = head['repo']['ssh_url']

    try:
        if sys.argv[2].lower() == 'push' if len(sys.argv) == 3 else False:
            push(origin, remote_branch_name, local_branch_name)
        else:
            pull(origin, remote_branch_name, local_branch_name)
    except CalledProcessError as e:
        print('error executing command: "{}"'.format(' '.join(e.cmd)))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
