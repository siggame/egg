import yaml
import shutil
from sh import git

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def grab(data, name):
    if 'type' not in data:
        raise KeyError('type not defined in %s in data.yaml' % name)
    if 'location' not in data:
        raise KeyError('location not defined in %s in data.yaml' % name)
    dest = '.components/%s' % name
    print('Grabbing %s from %s' % (name, data['location']))
    if data['type'] == 'git':
        git.clone(data['location'], dest)

def grab_components(location = 'components.yaml'):
        f = open(location)
        data = yaml.load(f, Loader)
        if 'codegen' not in data:
            raise KeyError('codegen not defined in data.yaml')

        try:
            shutil.rmtree('.components')
        except OSError:
            #Don't worry if the directory doesn't exist
            pass

        codegen = data.get('codegen')
        components = data.get('components', {})
        templates = data.get('templates', {})

        grab(data['codegen'], 'codegen')
        for key, value in components.items():
            grab(value, key)
        for key, value in templates.items():
            grab(value, key)


