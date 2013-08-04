from sh import git, ErrorReturnCode
import sys
import grabber
import maker


if __name__ == '__main__':
    try:
        git.show('master:data.yaml', _tty_out=False)
    except ErrorReturnCode:
        print('Error: data.yaml not committed to master')
        sys.exit(1)
    grabber.grab_components()
    git.checkout('-b', 'run-codegen')
    git.checkout('master', '--', 'data.yaml')

    maker.make_all()
    #git.add('-A')
    #git.commit(message = 'codegen rerun')
    #git.checkout('master')
    #git.merge('run-codegen')

