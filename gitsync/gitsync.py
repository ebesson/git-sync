import os
from PyGitUp.git_wrapper import GitError
from PyGitUp.gitup import GitUp
from git import Repo
from utils import read_projects_from_json
from model import Project

GITSYNC_FILE = "projects.json"


class GitSync(object):

    def __init__(self):
        self.current_directory = os.getcwd()

    def sync_all(self):
        json_projects = read_projects_from_json(GITSYNC_FILE)
        projects = map(lambda json_project: Project(json_project),
                       json_projects)
        filter(lambda project: self.proccess(project), projects)

    def proccess(self, project):
        # Clone repo if need
        if not os.path.isdir(project.path):
            Repo.clone_from(url=project.url, to_path=project.path)

        #TODO(ebe) check if the directory contains .git

        try:
            self.sync(project)
        except Exception as e:
            print(e.message)

    def sync(self, project):
        os.chdir(project.path)
        try:
            GitUp().run()
        except GitError as e:
            raise e
        finally:
            os.chdir(self.current_directory)
