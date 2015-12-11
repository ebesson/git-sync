from git import Repo
import os
from PyGitUp.git_wrapper import GitError
from PyGitUp.gitup import GitUp
from termcolor import cprint


class GitSync(object):

    def __init__(self, current_directory, projects_provider):
        self.current_directory = current_directory
        self.projects = projects_provider.projects()

    def sync_all(self):
        return list(map(lambda project: self.proccess(project), self.projects))

    def _display_info(self, message, attrs=None):
        cprint(text=message, color='green', attrs=attrs)

    def _display_error(self, message):
        cprint(text=message, color='red', attrs=['bold'])

    def proccess(self, project):
        self._display_info("\n => Process project %s" % project.name,
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
        except Exception:
            self._display_error("An error occurred during update")
        finally:
            os.chdir(self.current_directory)

    def sync(self, project):
        self._display_info(" - Update")
        os.chdir(project.path)
        try:
            GitUp().run()
        except GitError:
            raise Exception("An error occurred during update")
