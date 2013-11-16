from flask import request, g, abort, url_for, jsonify, session, after_this_request
from flask.ext.classy import FlaskView,route
from yearplan import application
from models import Auth, User, Sheet, UserSheet, Event
from common import require_auth
from datetime import datetime, timedelta

class SheetView(FlaskView):

   decorators = [ require_auth ]
   
   def index(self):
      sheets = Sheet.objects( alive = True )
      
      return jsonify( ok=True,  objects=[ sheet.to_json() for sheet in sheets])
      
   def get(self, id):
      """ Get Sheet document with given id """
      sheet = Sheet.objects.get_or_404( id = id , alive=True)
      
      return jsonify(ok=True, objects=[ sheet.to_json() ]), 200

   def post(self):
      """ Create a Sheet with given JSON """
      if not request.json or 'user' not in request.json:
         abort(400)
      
      # how do we get the user ? from a session
      user = User.objects.get_or_404( id = request.json['user']['id'] )
      
      new_sheet = Sheet(name = request.json['name'],
                        description = request.json['description'],
                        location = request.json['location'],
                        phone = request.json['phone'],
                        public = request.json['public'],
                        created_by = user.id,
                        links = request.json['links'],
                        color = request.json['color']
                       )
      new_sheet.tags = request.json['tags']
      new_sheet.alive = True
      new_sheet.save()
      # connect the user to the new sheet
      user_sheet = UserSheet( name=new_sheet.name, user=user, sheet=new_sheet, alive=True )
      user_sheet.save()
            
      return jsonify(ok=True, objects=[ user_sheet.to_json() ]), 200

   def put(self, id):
      """  @todo Save Current data in History """
      """ Update sheet data and save current data in history  """
      sheet = Sheet.objects.get_or_404( id = id )
      sheet.name = request.json['name']
      sheet.description = request.json['description']
      sheet.location = request.json['location']
      sheet.phone = request.json['phone']
      sheet.public = request.json['public']
      sheet.links = request.json['links']
      sheet.color = request.json['color']
      sheet.tags = request.json['tags']
      sheet.alive = True
      sheet.history.append( sheet )
      sheet.updated_at = datetime.now()
      sheet.save()
      
      return jsonify(ok=True), 200

   def delete(self, id):
      """ Mark sheet as deleted """
      sheet = Sheet.objects.get_or_404( id = id )
      sheet.deleted_at = datetime.now()
      sheet.history.append( sheet )
      sheet.alive = False
      sheet.save()      
      return jsonify(ok=True), 200

   @route('/<string:id>/users/<string:user_id>', methods=['POST'])
   def users(self, id, user_id ):
      """ Add the user given in the JSON to the sheet"""
      
      if 'user' not in request.json :
         abort(400)
      
      _sheet = Sheet.objects.get_or_404( id = id )
      _user = User.objects.get_or_404( id = id )
      
      user_sheet = UserSheet( name=sheet.name,user=_user, sheet=_sheet, alive=True)
      user_sheet.save()
      
      return jsonify(ok=True, objects=[user_sheet]), 200

   @route('/<string:id>/event/', methods=['GET','POST'])
   def sheet_event(self, id):
      """ Create an event """
      sheet = Sheet.objects.get_or_404(id = id )
      if request.method == 'GET' :
         """ Get all events """
         #if 'from' not in  request.args or 'to' not in request.args:
         #   abort(400, error = 'missing arguments from and to ')
         
         _sheetEvents = Event.objects(sheet=sheet, alive=True)
         
         _events = [e.to_json() for e in _sheetEvents ]
         return jsonify(ok=True, objects=[ _events ]),200
      
      if request.method == 'POST':
         
         new_event = Event( 
               dates = request.json['dates'],
               name = request.json['name'],
               description = request.json['description'],
               location = request.json['location'],
               public = request.json['public'],
               links = request.json['links'],
               color = request.json['color'],
               tags = request.json['tags'],
               alive = True,
               created_by = str(sheet.created_by),
               sheet= sheet
         )
         new_event.save()
         
         return jsonify(ok=True,objects=[new_event.to_json()]), 201

   # /sheet/trash
   def trash(self):
      """Recently deleted sheets within past 24hrs
          
          Users can see recently deleted events for a
         period of 24 hours and undelete them.
      """
      if request.method != 'GET' :
        abort(405)

      _trashed = Sheet.objects(alive=False,
                               updated_at__lte=datetime.now(),
                               updated_at__gte= (datetime.now() - timedelta(1))
                              )
      return jsonify(ok=True, objects=[item.to_json() for item in _trashed]),200

   @route('/<string:id>/event/trash', methods=['GET'])
   def event_trash(self, id):
      """ events recently deleted from this sheet within the last 24 hrs """
      sheet = Sheet.objects.get_or_404( id = id, alive=True)
      
      trashed = Event.objects(
                     alive = False,
                     sheet = sheet,
                     updated_at__lte = datetime.now(),
                     updated_at__gte = ( datetime.now() -timedelta(1) )
                  )
      return jsonify(ok=True, objects=[item.to_json() for item in trashed]),200
      
   @route('/<string:id>/users/<string:user_id>', methods = ['PUT', 'GET'])
   def preferences(self, id, user_id):
      """Update the user-sheet preferences 
         Users can 'star' the sheet by setting starred=true
      """
      sheet = Sheet.objects.get_or_404(id=id, alive=True)
      user = User.objects.get_or_404(id=id,alive=True)
      
      user_sheet = UserSheet.get_or_404( sheet=sheet,user=user, alive=True)
      
      if request.method == 'GET' :
         return jsonify(ok=True, objects=[user_sheet.to_json()]),200
         
      if request.method == 'PUT' :
         user_sheet.starred = request.json['starred']
         user_sheet.updated_at = datetime.now()
         user_sheet.history.append( user_sheet )
         user_sheet.save()
         return jsonify(ok=True), 200

