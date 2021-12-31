#!/usr/bin/env python3

import os
from configparser import RawConfigParser

__all__ = [
    "routine_config_file",
    "url_config_file",
    "dir_config_file",
    "ConfigHelper"
]

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
routine_config_file = os.path.join(project_dir, 'config/routine.ini')
url_config_file = os.path.join(project_dir, 'config/url.ini')

class ConfigHelper:

    def __init__(self, config_file: str):
        """ config instance init
        :param config_file: config file
        """
        self.config_file = config_file
        self.parser = RawConfigParser()
        self.parser.read(config_file)

    def read_config(self, section, key):
        """ read config from file
        :param section: section
        :param key: key
        :return: value
        """
        if section not in self.parser.sections():
            raise Exception("error")
        if key not in self.parser[section].keys():
            raise Exception("error")

        return self.parser[section][key]

    def write_config(self, section, key, value):
        """ write configuration to file
        :param section: section
        :param key: key
        :param value: value
        :return: none
        """
        self.parser.set(section, key, value)
        with open(self.config_file, 'w') as f:
            self.parser.write(f)