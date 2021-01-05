import os

from mchub.settings import BASE_DIR

def create_user(name):
    os.mkdir(os.path.join(BASE_DIR, 'projects', name))

def create_project(name, proj):
    os.mkdir(os.path.join(BASE_DIR, 'projects', name, proj))

def exist(name, proj):
    return os.path.isdir(os.path.join(BASE_DIR, 'projects', name, proj))

def get_proj(name):
    return os.listdir(os.path.join(BASE_DIR, 'projects', name))
