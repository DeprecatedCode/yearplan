from yearplan import application
from flask import session, abort, request, g, jsonify
from models import Auth

def require_auth(f):
   def decorator( *args, **kwargs ):
      # 'yearplan_user' not in request.cookies or
      if 'x-yearplan-user' not in request.headers:
         abort( 401 )
      try:
         auth = Auth.objects.get( alive=True, hash=request.headers['x-yearplan-user'])
      except(DoesNotExist):
         abort(401)
      return f( *args, **kwargs )
   return decorator