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


class Hooks(BaseClient):
    """
    Hooks are a mechanism for creating tasks in response to events.

    Hooks are identified with a `hookGroupId` and a `hookId`.

    When an event occurs, the resulting task is automatically created.  The
    task is created using the scope `assume:hook-id:<hookGroupId>/<hookId>`,
    which must have scopes to make the createTask call, including satisfying all
    scopes in `task.scopes`.  The new task has a `taskGroupId` equal to its
    `taskId`, as is the convention for decision tasks.

    Hooks can have a "schedule" indicating specific times that new tasks should
    be created.  Each schedule is in a simple cron format, per
    https://www.npmjs.com/package/cron-parser.  For example:
     * `['0 0 1 * * *']` -- daily at 1:00 UTC
     * `['0 0 9,21 * * 1-5', '0 0 12 * * 0,6']` -- weekdays at 9:00 and 21:00 UTC, weekends at noon
    """

    classOptions = {
        "baseUrl": "https://hooks.taskcluster.net/v1"
    }

    def listHookGroups(self, *args, **kwargs):
        """
        List hook groups

        This endpoint will return a list of all hook groups with at least one hook.

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/list-hook-groups-response.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["listHookGroups"], *args, **kwargs)

    def listHooks(self, *args, **kwargs):
        """
        List hooks in a given group

        This endpoint will return a list of all the hook definitions within a
        given hook group.

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/list-hooks-response.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["listHooks"], *args, **kwargs)

    def hook(self, *args, **kwargs):
        """
        Get hook definition

        This endpoint will return the hook defintion for the given `hookGroupId`
        and hookId.

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/hook-definition.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["hook"], *args, **kwargs)

    def getHookStatus(self, *args, **kwargs):
        """
        Get hook status

        This endpoint will return the current status of the hook.  This represents a
        snapshot in time and may vary from one call to the next.

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/hook-status.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["getHookStatus"], *args, **kwargs)

    def getHookSchedule(self, *args, **kwargs):
        """
        Get hook schedule

        This endpoint will return the schedule and next scheduled creation time
        for the given hook.

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/hook-schedule.json``

        This method is ``deprecated``
        """

        return self._makeApiCall(self.funcinfo["getHookSchedule"], *args, **kwargs)

    def createHook(self, *args, **kwargs):
        """
        Create a hook

        This endpoint will create a new hook.

        The caller's credentials must include the role that will be used to
        create the task.  That role must satisfy task.scopes as well as the
        necessary scopes to add the task to the queue.


        This method takes input: ``http://schemas.taskcluster.net/hooks/v1/create-hook-request.json``

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/hook-definition.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["createHook"], *args, **kwargs)

    def updateHook(self, *args, **kwargs):
        """
        Update a hook

        This endpoint will update an existing hook.  All fields except
        `hookGroupId` and `hookId` can be modified.

        This method takes input: ``http://schemas.taskcluster.net/hooks/v1/create-hook-request.json``

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/hook-definition.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["updateHook"], *args, **kwargs)

    def removeHook(self, *args, **kwargs):
        """
        Delete a hook

        This endpoint will remove a hook definition.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["removeHook"], *args, **kwargs)

    def triggerHook(self, *args, **kwargs):
        """
        Trigger a hook

        This endpoint will trigger the creation of a task from a hook definition.

        This method takes input: ``http://schemas.taskcluster.net/hooks/v1/trigger-payload.json``

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/task-status.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["triggerHook"], *args, **kwargs)

    def getTriggerToken(self, *args, **kwargs):
        """
        Get a trigger token

        Retrieve a unique secret token for triggering the specified hook. This
        token can be deactivated with `resetTriggerToken`.

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/trigger-token-response.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["getTriggerToken"], *args, **kwargs)

    def resetTriggerToken(self, *args, **kwargs):
        """
        Reset a trigger token

        Reset the token for triggering a given hook. This invalidates token that
        may have been issued via getTriggerToken with a new token.

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/trigger-token-response.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["resetTriggerToken"], *args, **kwargs)

    def triggerHookWithToken(self, *args, **kwargs):
        """
        Trigger a hook with a token

        This endpoint triggers a defined hook with a valid token.

        This method takes input: ``http://schemas.taskcluster.net/hooks/v1/trigger-payload.json``

        This method takes output: ``http://schemas.taskcluster.net/hooks/v1/task-status.json``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["triggerHookWithToken"], *args, **kwargs)

    def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    funcinfo = {
        "getTriggerToken": {           'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'getTriggerToken',
            'output': 'http://schemas.taskcluster.net/hooks/v1/trigger-token-response.json',
            'route': '/hooks/<hookGroupId>/<hookId>/token',
            'stability': 'experimental'},
        "listHooks": {           'args': ['hookGroupId'],
            'method': 'get',
            'name': 'listHooks',
            'output': 'http://schemas.taskcluster.net/hooks/v1/list-hooks-response.json',
            'route': '/hooks/<hookGroupId>',
            'stability': 'experimental'},
        "removeHook": {           'args': ['hookGroupId', 'hookId'],
            'method': 'delete',
            'name': 'removeHook',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'experimental'},
        "updateHook": {           'args': ['hookGroupId', 'hookId'],
            'input': 'http://schemas.taskcluster.net/hooks/v1/create-hook-request.json',
            'method': 'post',
            'name': 'updateHook',
            'output': 'http://schemas.taskcluster.net/hooks/v1/hook-definition.json',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'experimental'},
        "triggerHook": {           'args': ['hookGroupId', 'hookId'],
            'input': 'http://schemas.taskcluster.net/hooks/v1/trigger-payload.json',
            'method': 'post',
            'name': 'triggerHook',
            'output': 'http://schemas.taskcluster.net/hooks/v1/task-status.json',
            'route': '/hooks/<hookGroupId>/<hookId>/trigger',
            'stability': 'experimental'},
        "resetTriggerToken": {           'args': ['hookGroupId', 'hookId'],
            'method': 'post',
            'name': 'resetTriggerToken',
            'output': 'http://schemas.taskcluster.net/hooks/v1/trigger-token-response.json',
            'route': '/hooks/<hookGroupId>/<hookId>/token',
            'stability': 'experimental'},
        "ping": {           'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable'},
        "triggerHookWithToken": {           'args': ['hookGroupId', 'hookId', 'token'],
            'input': 'http://schemas.taskcluster.net/hooks/v1/trigger-payload.json',
            'method': 'post',
            'name': 'triggerHookWithToken',
            'output': 'http://schemas.taskcluster.net/hooks/v1/task-status.json',
            'route': '/hooks/<hookGroupId>/<hookId>/trigger/<token>',
            'stability': 'experimental'},
        "hook": {           'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'hook',
            'output': 'http://schemas.taskcluster.net/hooks/v1/hook-definition.json',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'experimental'},
        "createHook": {           'args': ['hookGroupId', 'hookId'],
            'input': 'http://schemas.taskcluster.net/hooks/v1/create-hook-request.json',
            'method': 'put',
            'name': 'createHook',
            'output': 'http://schemas.taskcluster.net/hooks/v1/hook-definition.json',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'experimental'},
        "listHookGroups": {           'args': [],
            'method': 'get',
            'name': 'listHookGroups',
            'output': 'http://schemas.taskcluster.net/hooks/v1/list-hook-groups-response.json',
            'route': '/hooks',
            'stability': 'experimental'},
        "getHookSchedule": {           'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'getHookSchedule',
            'output': 'http://schemas.taskcluster.net/hooks/v1/hook-schedule.json',
            'route': '/hooks/<hookGroupId>/<hookId>/schedule',
            'stability': 'deprecated'},
        "getHookStatus": {           'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'getHookStatus',
            'output': 'http://schemas.taskcluster.net/hooks/v1/hook-status.json',
            'route': '/hooks/<hookGroupId>/<hookId>/status',
            'stability': 'experimental'},
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Hooks']
