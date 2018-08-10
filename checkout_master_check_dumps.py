import os
try:
    from devtools import sformat
except ModuleNotFoundError:
    pass
else:
    dump_files = [fn for fn in os.listdir('.') if '.dump' in fn]
    if dump_files:
        print()
        print('\n'.join(dump_files))
        i = input(sformat('You have backups here. Would you like to delete them? [y]/n ', sformat.bold))
        if not i or i == 'y':
            for fn in dump_files:
                os.system('shred -uz ' + fn)
                print('Shredded ' + fn)
os.system('git checkout master')
