import os
import shutil

from yaml import full_load

from exceptions import ConfigNotFoundException

def handle_local_dir(path):
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    if not os.path.exists(full_path):
        os.mkdir(full_path)
        print('Created directory {path}'.format(path=full_path))
    else:
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            try:
                shutil.rmtree(file_path)
            except OSError:
                os.remove(file_path)


def get_config(path):
    if os.path.exists(path):
        with open(path) as file:
            config = full_load(file)
    else:
        raise ConfigNotFoundException('Config not found at {path}'.format(
            path=path
        ))

    return config