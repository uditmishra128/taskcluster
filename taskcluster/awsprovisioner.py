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


class AwsProvisioner(BaseClient):
    """
    The AWS Provisioner is responsible for provisioning instances on EC2 for use in
    TaskCluster.  The provisioner maintains a set of worker configurations which
    can be managed with an API that is typically available at
    aws-provisioner.taskcluster.net/v1.  This API can also perform basic instance
    management tasks in addition to maintaining the internal state of worker type
    configuration information.

    The Provisioner runs at a configurable interval.  Each iteration of the
    provisioner fetches a current copy the state that the AWS EC2 api reports.  In
    each iteration, we ask the Queue how many tasks are pending for that worker
    type.  Based on the number of tasks pending and the scaling ratio, we may
    submit requests for new instances.  We use pricing information, capacity and
    utility factor information to decide which instance type in which region would
    be the optimal configuration.

    Each EC2 instance type will declare a capacity and utility factor.  Capacity is
    the number of tasks that a given machine is capable of running concurrently.
    Utility factor is a relative measure of performance between two instance types.
    We multiply the utility factor by the spot price to compare instance types and
    regions when making the bidding choices.

    When a new EC2 instance is instantiated, its user data contains a token in
    `securityToken` that can be used with the `getSecret` method to retrieve
    the worker's credentials and any needed passwords or other restricted
    information.  The worker is responsible for deleting the secret after
    retrieving it, to prevent dissemination of the secret to other proceses
    which can read the instance user data.

    """

    classOptions = {
        "baseUrl": "https://aws-provisioner.taskcluster.net/v1"
    }

    def listWorkerTypeSummaries(self, *args, **kwargs):
        """
        List worker types with details

        Return a list of worker types, including some summary information about
        current capacity for each.  While this list includes all defined worker types,
        there may be running EC2 instances for deleted worker types that are not
        included here.  The list is unordered.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/list-worker-types-summaries-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["listWorkerTypeSummaries"], *args, **kwargs)

    def createWorkerType(self, *args, **kwargs):
        """
        Create new Worker Type

        Create a worker type.  A worker type contains all the configuration
        needed for the provisioner to manage the instances.  Each worker type
        knows which regions and which instance types are allowed for that
        worker type.  Remember that Capacity is the number of concurrent tasks
        that can be run on a given EC2 resource and that Utility is the relative
        performance rate between different instance types.  There is no way to
        configure different regions to have different sets of instance types
        so ensure that all instance types are available in all regions.
        This function is idempotent.

        Once a worker type is in the provisioner, a back ground process will
        begin creating instances for it based on its capacity bounds and its
        pending task count from the Queue.  It is the worker's responsibility
        to shut itself down.  The provisioner has a limit (currently 96hours)
        for all instances to prevent zombie instances from running indefinitely.

        The provisioner will ensure that all instances created are tagged with
        aws resource tags containing the provisioner id and the worker type.

        If provided, the secrets in the global, region and instance type sections
        are available using the secrets api.  If specified, the scopes provided
        will be used to generate a set of temporary credentials available with
        the other secrets.

        This method takes input: ``http://schemas.taskcluster.net/aws-provisioner/v1/create-worker-type-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["createWorkerType"], *args, **kwargs)

    def updateWorkerType(self, *args, **kwargs):
        """
        Update Worker Type

        Provide a new copy of a worker type to replace the existing one.
        This will overwrite the existing worker type definition if there
        is already a worker type of that name.  This method will return a
        200 response along with a copy of the worker type definition created
        Note that if you are using the result of a GET on the worker-type
        end point that you will need to delete the lastModified and workerType
        keys from the object returned, since those fields are not allowed
        the request body for this method

        Otherwise, all input requirements and actions are the same as the
        create method.

        This method takes input: ``http://schemas.taskcluster.net/aws-provisioner/v1/create-worker-type-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["updateWorkerType"], *args, **kwargs)

    def workerTypeLastModified(self, *args, **kwargs):
        """
        Get Worker Type Last Modified Time

        This method is provided to allow workers to see when they were
        last modified.  The value provided through UserData can be
        compared against this value to see if changes have been made
        If the worker type definition has not been changed, the date
        should be identical as it is the same stored value.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-last-modified.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["workerTypeLastModified"], *args, **kwargs)

    def workerType(self, *args, **kwargs):
        """
        Get Worker Type

        Retreive a copy of the requested worker type definition.
        This copy contains a lastModified field as well as the worker
        type name.  As such, it will require manipulation to be able to
        use the results of this method to submit date to the update
        method.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["workerType"], *args, **kwargs)

    def removeWorkerType(self, *args, **kwargs):
        """
        Delete Worker Type

        Delete a worker type definition.  This method will only delete
        the worker type definition from the storage table.  The actual
        deletion will be handled by a background worker.  As soon as this
        method is called for a worker type, the background worker will
        immediately submit requests to cancel all spot requests for this
        worker type as well as killing all instances regardless of their
        state.  If you want to gracefully remove a worker type, you must
        either ensure that no tasks are created with that worker type name
        or you could theoretically set maxCapacity to 0, though, this is
        not a supported or tested action

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["removeWorkerType"], *args, **kwargs)

    def listWorkerTypes(self, *args, **kwargs):
        """
        List Worker Types

        Return a list of string worker type names.  These are the names
        of all managed worker types known to the provisioner.  This does
        not include worker types which are left overs from a deleted worker
        type definition but are still running in AWS.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/list-worker-types-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["listWorkerTypes"], *args, **kwargs)

    def createAmiSet(self, *args, **kwargs):
        """
        Create new AMI Set

        Create an AMI Set. An AMI Set is a collection of AMIs with a single name.

        This method takes input: ``http://schemas.taskcluster.net/aws-provisioner/v1/create-ami-set-request.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["createAmiSet"], *args, **kwargs)

    def amiSet(self, *args, **kwargs):
        """
        Get AMI Set

        Retreive a copy of the requested AMI set.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-ami-set-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["amiSet"], *args, **kwargs)

    def updateAmiSet(self, *args, **kwargs):
        """
        Update AMI Set

        Provide a new copy of an AMI Set to replace the existing one.
        This will overwrite the existing AMI Set if there
        is already an AMI Set of that name. This method will return a
        200 response along with a copy of the AMI Set created.
        Note that if you are using the result of a GET on the ami-set
        end point that you will need to delete the lastModified and amiSet
        keys from the object returned, since those fields are not allowed
        the request body for this method.

        Otherwise, all input requirements and actions are the same as the
        create method.

        This method takes input: ``http://schemas.taskcluster.net/aws-provisioner/v1/create-ami-set-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-ami-set-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["updateAmiSet"], *args, **kwargs)

    def listAmiSets(self, *args, **kwargs):
        """
        List AMI sets

        Return a list of AMI sets names.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/list-ami-sets-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["listAmiSets"], *args, **kwargs)

    def removeAmiSet(self, *args, **kwargs):
        """
        Delete AMI Set

        Delete an AMI Set.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["removeAmiSet"], *args, **kwargs)

    def createSecret(self, *args, **kwargs):
        """
        Create new Secret

        Insert a secret into the secret storage.  The supplied secrets will
        be provided verbatime via `getSecret`, while the supplied scopes will
        be converted into credentials by `getSecret`.

        This method is not ordinarily used in production; instead, the provisioner
        creates a new secret directly for each spot bid.

        This method takes input: ``http://schemas.taskcluster.net/aws-provisioner/v1/create-secret-request.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["createSecret"], *args, **kwargs)

    def getSecret(self, *args, **kwargs):
        """
        Get a Secret

        Retrieve a secret from storage.  The result contains any passwords or
        other restricted information verbatim as well as a temporary credential
        based on the scopes specified when the secret was created.

        It is important that this secret is deleted by the consumer (`removeSecret`),
        or else the secrets will be visible to any process which can access the
        user data associated with the instance.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-secret-response.json#``

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["getSecret"], *args, **kwargs)

    def instanceStarted(self, *args, **kwargs):
        """
        Report an instance starting

        An instance will report in by giving its instance id as well
        as its security token.  The token is given and checked to ensure
        that it matches a real token that exists to ensure that random
        machines do not check in.  We could generate a different token
        but that seems like overkill

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["instanceStarted"], *args, **kwargs)

    def removeSecret(self, *args, **kwargs):
        """
        Remove a Secret

        Remove a secret.  After this call, a call to `getSecret` with the given
        token will return no information.

        It is very important that the consumer of a
        secret delete the secret from storage before handing over control
        to untrusted processes to prevent credential and/or secret leakage.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["removeSecret"], *args, **kwargs)

    def getLaunchSpecs(self, *args, **kwargs):
        """
        Get All Launch Specifications for WorkerType

        This method returns a preview of all possible launch specifications
        that this worker type definition could submit to EC2.  It is used to
        test worker types, nothing more

        **This API end-point is experimental and may be subject to change without warning.**

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/get-launch-specs-response.json#``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["getLaunchSpecs"], *args, **kwargs)

    def state(self, *args, **kwargs):
        """
        Get AWS State for a worker type

        Return the state of a given workertype as stored by the provisioner.
        This state is stored as three lists: 1 for running instances, 1 for
        pending requests.  The `summary` property contains an updated summary
        similar to that returned from `listWorkerTypeSummaries`.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["state"], *args, **kwargs)

    def ping(self, *args, **kwargs):
        """
        Ping Server

        Documented later...

        **Warning** this api end-point is **not stable**.

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    def backendStatus(self, *args, **kwargs):
        """
        Backend Status

        This endpoint is used to show when the last time the provisioner
        has checked in.  A check in is done through the deadman's snitch
        api.  It is done at the conclusion of a provisioning iteration
        and used to tell if the background provisioning process is still
        running.

        **Warning** this api end-point is **not stable**.

        This method takes output: ``http://schemas.taskcluster.net/aws-provisioner/v1/backend-status-response.json#``

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["backendStatus"], *args, **kwargs)

    def terminateAllInstancesOfWorkerType(self, *args, **kwargs):
        """
        Shutdown Every Ec2 Instance of this Worker Type

        WARNING: YOU ALMOST CERTAINLY DO NOT WANT TO USE THIS
        Shut down every single EC2 instance associated with this workerType.
        This means every single last one.  You probably don't want to use
        this method, which is why it has an obnoxious name.  Don't even try
        to claim you didn't know what this method does!

        **This API end-point is experimental and may be subject to change without warning.**

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["terminateAllInstancesOfWorkerType"], *args, **kwargs)

    def shutdownEverySingleEc2InstanceManagedByThisProvisioner(self, *args, **kwargs):
        """
        Shutdown Every Single Ec2 Instance Managed By This Provisioner

        WARNING: YOU ALMOST CERTAINLY DO NOT WANT TO USE THIS
        Shut down every single EC2 instance managed by this provisioner.
        This means every single last one.  You probably don't want to use
        this method, which is why it has an obnoxious name.  Don't even try
        to claim you didn't know what this method does!

        **This API end-point is experimental and may be subject to change without warning.**

        This method is ``experimental``
        """

        return self._makeApiCall(self.funcinfo["shutdownEverySingleEc2InstanceManagedByThisProvisioner"], *args, **kwargs)

    funcinfo = {
        "terminateAllInstancesOfWorkerType": {           'args': ['workerType'],
            'method': 'post',
            'name': 'terminateAllInstancesOfWorkerType',
            'route': '/worker-type/<workerType>/terminate-all-instances',
            'stability': 'experimental'},
        "backendStatus": {           'args': [],
            'method': 'get',
            'name': 'backendStatus',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/backend-status-response.json#',
            'route': '/backend-status',
            'stability': 'experimental'},
        "listWorkerTypes": {           'args': [],
            'method': 'get',
            'name': 'listWorkerTypes',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/list-worker-types-response.json#',
            'route': '/list-worker-types',
            'stability': 'stable'},
        "getSecret": {           'args': ['token'],
            'method': 'get',
            'name': 'getSecret',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-secret-response.json#',
            'route': '/secret/<token>',
            'stability': 'stable'},
        "ping": {           'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'experimental'},
        "workerType": {           'args': ['workerType'],
            'method': 'get',
            'name': 'workerType',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-response.json#',
            'route': '/worker-type/<workerType>',
            'stability': 'stable'},
        "listWorkerTypeSummaries": {           'args': [],
            'method': 'get',
            'name': 'listWorkerTypeSummaries',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/list-worker-types-summaries-response.json#',
            'route': '/list-worker-type-summaries',
            'stability': 'stable'},
        "shutdownEverySingleEc2InstanceManagedByThisProvisioner": {           'args': [],
            'method': 'post',
            'name': 'shutdownEverySingleEc2InstanceManagedByThisProvisioner',
            'route': '/shutdown/every/single/ec2/instance/managed/by/this/provisioner',
            'stability': 'experimental'},
        "removeWorkerType": {           'args': ['workerType'],
            'method': 'delete',
            'name': 'removeWorkerType',
            'route': '/worker-type/<workerType>',
            'stability': 'stable'},
        "removeSecret": {           'args': ['token'],
            'method': 'delete',
            'name': 'removeSecret',
            'route': '/secret/<token>',
            'stability': 'stable'},
        "updateAmiSet": {           'args': ['id'],
            'input': 'http://schemas.taskcluster.net/aws-provisioner/v1/create-ami-set-request.json#',
            'method': 'post',
            'name': 'updateAmiSet',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-ami-set-response.json#',
            'route': '/ami-set/<id>/update',
            'stability': 'stable'},
        "workerTypeLastModified": {           'args': ['workerType'],
            'method': 'get',
            'name': 'workerTypeLastModified',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-last-modified.json#',
            'route': '/worker-type-last-modified/<workerType>',
            'stability': 'stable'},
        "updateWorkerType": {           'args': ['workerType'],
            'input': 'http://schemas.taskcluster.net/aws-provisioner/v1/create-worker-type-request.json#',
            'method': 'post',
            'name': 'updateWorkerType',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-response.json#',
            'route': '/worker-type/<workerType>/update',
            'stability': 'stable'},
        "getLaunchSpecs": {           'args': ['workerType'],
            'method': 'get',
            'name': 'getLaunchSpecs',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-launch-specs-response.json#',
            'route': '/worker-type/<workerType>/launch-specifications',
            'stability': 'experimental'},
        "listAmiSets": {           'args': [],
            'method': 'get',
            'name': 'listAmiSets',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/list-ami-sets-response.json#',
            'route': '/list-ami-sets',
            'stability': 'stable'},
        "state": {           'args': ['workerType'],
            'method': 'get',
            'name': 'state',
            'route': '/state/<workerType>',
            'stability': 'stable'},
        "createAmiSet": {           'args': ['id'],
            'input': 'http://schemas.taskcluster.net/aws-provisioner/v1/create-ami-set-request.json#',
            'method': 'put',
            'name': 'createAmiSet',
            'route': '/ami-set/<id>',
            'stability': 'stable'},
        "createWorkerType": {           'args': ['workerType'],
            'input': 'http://schemas.taskcluster.net/aws-provisioner/v1/create-worker-type-request.json#',
            'method': 'put',
            'name': 'createWorkerType',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-worker-type-response.json#',
            'route': '/worker-type/<workerType>',
            'stability': 'stable'},
        "removeAmiSet": {           'args': ['id'],
            'method': 'delete',
            'name': 'removeAmiSet',
            'route': '/ami-set/<id>',
            'stability': 'stable'},
        "amiSet": {           'args': ['id'],
            'method': 'get',
            'name': 'amiSet',
            'output': 'http://schemas.taskcluster.net/aws-provisioner/v1/get-ami-set-response.json#',
            'route': '/ami-set/<id>',
            'stability': 'stable'},
        "createSecret": {           'args': ['token'],
            'input': 'http://schemas.taskcluster.net/aws-provisioner/v1/create-secret-request.json#',
            'method': 'put',
            'name': 'createSecret',
            'route': '/secret/<token>',
            'stability': 'stable'},
        "instanceStarted": {           'args': ['instanceId', 'token'],
            'method': 'get',
            'name': 'instanceStarted',
            'route': '/instance-started/<instanceId>/<token>',
            'stability': 'stable'},
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'AwsProvisioner']
