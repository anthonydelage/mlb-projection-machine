import os
import argparse

from utils import get_config, handle_local_dir
from fangraphs import download_projections

DATA_DIR = '../data'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        help='Configuration file location',
        action='store',
        required=True
    )
    args = parser.parse_args()
    config = get_config(args.config)

    handle_local_dir(DATA_DIR)

    download_projections(config['systems'], DATA_DIR)


if __name__ == '__main__':
    main()
