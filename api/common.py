from flask import session, abort

def require_auth(f):
   def decorator( *args, **kwargs ):
      if 'yearplan_user' not in session:
         abort( 401 )
      
      return f( *args, **kwargs )
   return decorator