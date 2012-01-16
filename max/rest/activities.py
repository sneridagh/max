from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotImplemented

from max.MADMax import MADMaxDB
from max.models import Activity
from max.decorators import MaxRequest, MaxResponse

from max.rest.ResourceHandlers import JSONResourceRoot, JSONResourceEntity


@view_config(route_name='user_activities', request_method='GET')
@MaxResponse
@MaxRequest
def getUserActivities(context, request):
    """
         /people/{displayName}/activities

         Retorna all activities generated by a user
    """
    displayName = request.matchdict['displayName']

    mmdb = MADMaxDB(context.db)

    actor = mmdb.users.getItemsBydisplayName(displayName)[0]

    query = {'actor._id': actor['_id']}
    activities = mmdb.activity.search(query, sort="_id", flatten=1)

    handler = JSONResourceRoot(activities)
    return handler.buildResponse()


@view_config(route_name='user_activities', request_method='POST')
@MaxResponse
@MaxRequest
def addUserActivity(context, request):
    """
         /users/{displayName}/activities

         Afegeix una activitat
    """
    displayName = request.matchdict['displayName']

    mmdb = MADMaxDB(context.db)
    actor = mmdb.users.getItemsBydisplayName(displayName)[0]
    rest_params = {'actor': actor}

    # Initialize a Activity object from the request
    newactivity = Activity(request, rest_params=rest_params)

    # If we have the _id setted, then the object already existed in the DB,
    # otherwise, proceed to insert it into the DB
    # In both cases, respond with the JSON of the object and the appropiate
    # HTTP Status Code

    if newactivity.get('_id'):
        # Already Exists
        code = 200
    else:
        # New User
        code = 201
        activity_oid = newactivity.insert()
        newactivity['_id'] = activity_oid

    handler = JSONResourceEntity(newactivity.flatten(), status_code=code)
    return handler.buildResponse()


@view_config(route_name='activities', request_method='GET')
def getActivities(context, request):
    """
         /activities

         Retorna all activities
    """
    return HTTPNotImplemented()


@view_config(route_name='activity', request_method='GET')
#@MaxResponse
#@MaxRequest
def getActivity(context, request):
    """
         /activities/{activity}

         Mostra una activitat
    """

    mmdb = MADMaxDB(context.db)
    activity_oid = request.matchdict['activity']
    activity = mmdb.activity[activity_oid].flatten()

    handler = JSONResourceEntity(activity)
    return handler.buildResponse()


@view_config(route_name='activity', request_method='DELETE')
def deleteActivity(context, request):
    """
    """
    return HTTPNotImplemented()


@view_config(route_name='activity', request_method='PUT')
def modifyActivity(context, request):
    """
    """
    return HTTPNotImplemented()
