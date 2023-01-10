import sys
import subprocess
import time
from dataclasses import dataclass


def current_window_id():
    pid = int(subprocess.check_output(['xdotool', 'getactivewindow']).splitlines()[0].decode())
    hex_pid = '0x{:08x}'.format(pid)
    return hex_pid


def matching_open_windows(search_name):
    matching_pids = [p for p in subprocess.check_output(['pgrep', search_name]).decode().splitlines()]
    for w in [l.split() for l in subprocess.check_output(["wmctrl", "-lp"]).splitlines()]:
        pid = w[2].decode()
        if pid in matching_pids:
            yield w[0].decode()


def run():
    if len(sys.argv) < 2:
        print('usage: ./get_or_create_app.py <app_name>')
        return 1
    search_name = launch_name = focus_name = sys.argv[1]
    if search_name == 'chrome':
        launch_name = 'google-chrome'
    elif search_name == 'java':
        launch_name = 'pycharm-professional'
        focus_name = 'jetbrains-pycharm'
    open_windows = sorted(list(matching_open_windows(search_name)))
    if open_windows:
        # Check to see if the window is already focussed.
        current_window = current_window_id()
        if current_window in open_windows:
            # If so, then cycle to the next window of it's type 
            try:
                next_window = open_windows[open_windows.index(current_window) + 1]
            except IndexError:
                next_window = open_windows[0]
            window_to_focus = next_window
        else:
            # Focus on that window
            window_to_focus = open_windows[0]
        subprocess.Popen(['wmctrl', '-ia', window_to_focus])
    else:
        # The app is not running
        subprocess.call(launch_name, shell=True)


if __name__ == '__main__':
    run()
