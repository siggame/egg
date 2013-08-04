from sh import git, python3, ErrorReturnCode
import shutil
import sys
import grabber


if __name__ == '__main__':
    try:
        git.show('master:data.yaml', _tty_out=False)
    except ErrorReturnCode:
        print('Error: data.yaml not committed to master')
        sys.exit(1)
    grabber.grab_components()

