# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from .client import BaseClient
from .client import createApiClient
from .client import config
from .client import createTemporaryCredentials
from .client import createSession
_defaultConfig = config


class Github(BaseClient):
    """
    The github service is responsible for creating tasks in reposnse
    to GitHub events, and posting results to the GitHub UI.

    This document describes the API end-point for consuming GitHub
    web hooks, as well as some useful consumer APIs.

    When Github forbids an action, this service returns an HTTP 403
    with code ForbiddenByGithub.
    """

    classOptions = {
    }
    serviceName = 'github'
    apiVersion = 'v1'

    def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    def githubWebHookConsumer(self, *args, **kwargs):
        """
        Consume GitHub WebHook

        Capture a GitHub event and publish it via pulse, if it's a push,
        release or pull request.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["githubWebHookConsumer"], *args, **kwargs)

    def builds(self, *args, **kwargs):
        """
        List of Builds

        A paginated list of builds that have been run in
        Taskcluster. Can be filtered on various git-specific
        fields.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["builds"], *args, **kwargs)

    def badge(self, *args, **kwargs):
        """
        Latest Build Status Badge

        Checks the status of the latest build of a given branch
        and returns corresponding badge svg.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["badge"], *args, **kwargs)

    def repository(self, *args, **kwargs):
        """
        Get Repository Info

        Returns any repository metadata that is
        useful within Taskcluster related services.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["repository"], *args, **kwargs)

    def latest(self, *args, **kwargs):
        """
        Latest Status for Branch

        For a given branch of a repository, this will always point
        to a status page for the most recent task triggered by that
        branch.

        Note: This is a redirect rather than a direct link.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["latest"], *args, **kwargs)

    def createStatus(self, *args, **kwargs):
        """
        Post a status against a given changeset

        For a given changeset (SHA) of a repository, this will attach a "commit status"
        on github. These statuses are links displayed next to each revision.
        The status is either OK (green check) or FAILURE (red cross),
        made of a custom title and link.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["createStatus"], *args, **kwargs)

    def createComment(self, *args, **kwargs):
        """
        Post a comment on a given GitHub Issue or Pull Request

        For a given Issue or Pull Request of a repository, this will write a new message.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["createComment"], *args, **kwargs)

    funcinfo = {
        "badge": {
            'args': ['owner', 'repo', 'branch'],
            'method': 'get',
            'name': 'badge',
            'route': '/repository/<owner>/<repo>/<branch>/badge.svg',
            'stability': 'experimental',
        },
        "builds": {
            'args': [],
            'method': 'get',
            'name': 'builds',
            'query': ['continuationToken', 'limit', 'organization', 'repository', 'sha'],
            'route': '/builds',
            'stability': 'experimental',
        },
        "createComment": {
            'args': ['owner', 'repo', 'number'],
            'method': 'post',
            'name': 'createComment',
            'route': '/repository/<owner>/<repo>/issues/<number>/comments',
            'stability': 'experimental',
        },
        "createStatus": {
            'args': ['owner', 'repo', 'sha'],
            'method': 'post',
            'name': 'createStatus',
            'route': '/repository/<owner>/<repo>/statuses/<sha>',
            'stability': 'experimental',
        },
        "githubWebHookConsumer": {
            'args': [],
            'method': 'post',
            'name': 'githubWebHookConsumer',
            'route': '/github',
            'stability': 'experimental',
        },
        "latest": {
            'args': ['owner', 'repo', 'branch'],
            'method': 'get',
            'name': 'latest',
            'route': '/repository/<owner>/<repo>/<branch>/latest',
            'stability': 'experimental',
        },
        "ping": {
            'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable',
        },
        "repository": {
            'args': ['owner', 'repo'],
            'method': 'get',
            'name': 'repository',
            'route': '/repository/<owner>/<repo>',
            'stability': 'experimental',
        },
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Github']
