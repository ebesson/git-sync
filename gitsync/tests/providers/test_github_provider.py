# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from gitsync.providers.github_provider import GithubProvider


class TestGithubProvider(TestCase):

    @patch("getpass.getpass")
    def test_password_is_asked(self, m_getpass):
        m_getpass.return_value = "passwd"
        self.github_user = "user"

        self.provider = GithubProvider(self.github_user)
        self.assertTrue(m_getpass.called)
