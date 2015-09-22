from git import Repo
from model import Project
import os
from PyGitUp.git_wrapper import GitError
from PyGitUp.gitup import GitUp
from termcolor import cprint
from utils import read_projects_from_json


GITSYNC_FILE = "git-sync.json"


class GitSync(object):
    def __init__(self):
        self.current_directory = os.getcwd()

    def sync_all(self):

        gitsync_path = os.path.join(self.current_directory, GITSYNC_FILE)
        if not os.path.isfile(gitsync_path):
            raise Exception("No such file projects.json in current directory")

        json_projects = read_projects_from_json(GITSYNC_FILE)
        projects = list(map(lambda json_project: Project(json_project),
                       json_projects))
        return list(map(lambda project: self.proccess(project), projects))

    def _display_info(self, message, attrs=None):
        cprint(text=message, color='green', attrs=attrs)

    def _display_error(self, message):
        cprint(text=message, color='red', attrs=['bold'])

    def proccess(self, project):
        self._display_info("=> Process project %s" % project.name,
                           attrs=['bold'])

        if not os.path.isdir(project.path):
            self._display_info(" - Cloning %s in directory %s" %
                               (project.url, project.path))
            Repo.clone_from(url=project.url, to_path=project.path)
            self._display_info(" - Clone successfull")

        dot_git_path = os.path.join(project.path, ".git")
        if not os.path.isdir(dot_git_path):
            raise Exception("The directory %s is not a git repository." %
                            project.path)

        try:
            self.sync(project)
            self._display_info(" - Update successfull")
        except:
            self._display_error("An error occurred during update")
        finally:
            os.chdir(self.current_directory)

    def sync(self, project):
        self._display_info(" - Update")
        os.chdir(project.path)
        try:
            GitUp().run()
        except GitError as e:
            raise Exception("An error occurred during update")
