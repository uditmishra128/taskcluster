# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from .asyncclient import AsyncBaseClient
from .asyncclient import createApiClient
from .asyncclient import config
from .asyncclient import createTemporaryCredentials
from .asyncclient import createSession
_defaultConfig = config


class Pulse(AsyncBaseClient):
    """
    The taskcluster-pulse service, typically available at `pulse.taskcluster.net`
    manages pulse credentials for taskcluster users.

    A service to manage Pulse credentials for anything using
    Taskcluster credentials. This allows for self-service pulse
    access and greater control within the Taskcluster project.
    """

    classOptions = {
    }
    serviceName = 'pulse'
    apiVersion = 'v1'

    async def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    async def listNamespaces(self, *args, **kwargs):
        """
        List Namespaces

        List the namespaces managed by this service.

        This will list up to 1000 namespaces. If more namespaces are present a
        `continuationToken` will be returned, which can be given in the next
        request. For the initial request, do not provide continuation token.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["listNamespaces"], *args, **kwargs)

    async def namespace(self, *args, **kwargs):
        """
        Get a namespace

        Get public information about a single namespace. This is the same information
        as returned by `listNamespaces`.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["namespace"], *args, **kwargs)

    async def claimNamespace(self, *args, **kwargs):
        """
        Claim a namespace

        Claim a namespace, returning a connection string with access to that namespace
        good for use until the `reclaimAt` time in the response body. The connection
        string can be used as many times as desired during this period, but must not
        be used after `reclaimAt`.

        Connections made with this connection string may persist beyond `reclaimAt`,
        although it should not persist forever.  24 hours is a good maximum, and this
        service will terminate connections after 72 hours (although this value is
        configurable).

        The specified `expires` time updates any existing expiration times.  Connections
        for expired namespaces will be terminated.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["claimNamespace"], *args, **kwargs)

    funcinfo = {
        "claimNamespace": {
            'args': ['namespace'],
            'method': 'post',
            'name': 'claimNamespace',
            'route': '/namespace/<namespace>',
            'stability': 'experimental',
        },
        "listNamespaces": {
            'args': [],
            'method': 'get',
            'name': 'listNamespaces',
            'query': ['limit', 'continuationToken'],
            'route': '/namespaces',
            'stability': 'experimental',
        },
        "namespace": {
            'args': ['namespace'],
            'method': 'get',
            'name': 'namespace',
            'route': '/namespace/<namespace>',
            'stability': 'experimental',
        },
        "ping": {
            'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable',
        },
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Pulse']
