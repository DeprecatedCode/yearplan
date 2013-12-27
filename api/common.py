from yearplan import application
from flask import session, abort, request, g, jsonify
from models import Auth

def require_auth (f):
    def decorator (*args, **kwargs):
        # check if 'token' not in request.cookies or
        if 'X-yearplan-user' not in request.headers:
            abort(401)
        try:
            # allow everyone for now
            auth = Auth.objects.get(alive=True, hash=request.headers['X-yearplan-user'])
        except(DoesNotExist):
            abort(401)
        return f(*args, **kwargs)
    return decorator

@application.errorhandler(400)
def bad_request(error):
   return jsonify(ok=False, errors= ['Bad Request.']), 400

@application.errorhandler(401)
def not_authorised(error):
   return jsonify(ok=False,errors=['Not authorised']), 401

@application.errorhandler(404)
def resource_not_found(error):
   return jsonify(ok=False, errors= ['Not found']), 404
   
@application.errorhandler(405)
def method_not_allowed(error):
   return jsonify(ok=False, errors= ['Method Not allowed']), 405
   
@application.errorhandler(410)
def resource_gone(error):
   return jsonify(ok=False, errors= ['Resource deleted']), 410

@application.errorhandler(501)
def not_implemented(error):
   return jsonify(ok=False, errors=['Not yet available in this version of the API']),501