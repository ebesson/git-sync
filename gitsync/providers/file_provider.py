# -*- coding: utf-8 -*-
import os

import yaml
from gitsync.model.project import Project
from gitsync.provider import Provider


GITSYNC_FILE = "git-sync.yml"


class FileProvider(Provider):

    def __init__(self):
        super(Provider, self).__init__()
        self.project_file = GITSYNC_FILE

    def _read_projects_from_yaml(self):
        file_handler = os.path.join(os.curdir, self.project_file)
        try:
            with open(file_handler) as json_file:
                projects = yaml.load(json_file)
        except Exception:
            raise Exception("Invalid yaml file...")
        return projects

    def projects(self):
        yaml_projects = self._read_projects_from_yaml()
        return list(map(lambda yaml_project: Project(yaml_project),
                        yaml_projects))

    def need_to_write_gitsync_file(self):
        return False
