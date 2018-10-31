
class Response():
    pass

known_good_logins = [('user1', 'pass')]

def post(uri, auth=(), data=''):

    if auth:
        if auth in known_good_logins:
            response = Response()
            response.status_code = 201
            response.content = '{"token": "dummy_token"}'
            return response
        else:
            response = Response()
            response.status_code = 500
            return response
