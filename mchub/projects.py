from json import dump, load
import os

from mchub.settings import BASE_DIR

def create_user(name):
    os.mkdir(os.path.join(BASE_DIR, 'projects', name))

def create_project(name, proj, desp='', website=''):
    os.mkdir(os.path.join(BASE_DIR, 'projects', name, proj))
    dump({
            'description': desp,
            'website': website
        }, open(os.path.join(BASE_DIR, 'projects', name, proj, 'configure.json'), 'w+'), indent='\t')

def exist(name, proj):
    return os.path.isdir(os.path.join(BASE_DIR, 'projects', name, proj))

def has_proj(name, proj):
    if not os.path.isdir(os.path.join(BASE_DIR, 'projects', name)):
        return False
    for d in os.listdir(os.path.join(BASE_DIR, 'projects', name)):
        if d == proj:
            return True
    else:
        return False

def get_configure(name, proj):
    return load(open(os.path.join(BASE_DIR, 'projects', name, proj, 'configure.json')))

def get_proj(name):
    return os.listdir(os.path.join(BASE_DIR, 'projects', name))
