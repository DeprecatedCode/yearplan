from flask import request, g, abort, jsonify
from flask.ext.classy import FlaskView
from models import User, Event, Sheet
from common import require_auth
from datetime import datetime

class EventView (FlaskView):
   
    decorators = [ require_auth ]

    def get(self, id):
        event = Event.objects.get_or_404(id=id, alive=True)
        
        return jsonify(ok=True, objects=[ event.to_json() ]),200

    def put(self, id):
        """ Get an events details
        Edit/Restore an event
        """
        event = Event.objects.get_or_404(id=id)
        event.event_date = request.json['event_date']
        event.dates = request.json['dates']
        event.name = request.json['name']
        event.description = request.json['description']
        event.location = request.json['location']
        event.public = request.json['public']
        event.links = request.json['links']
        event.color = request.json['color']
        event.tags = request.json['tags']
        event.alive = True
        # add current details to history
        event.history.append(event)
        event.updated_at = datetime.now()
        event.save()
        
        return jsonify(ok=True), 200

    def move(self,id):
        """ Move an event from one sheet to another """
        event = Event.objects.get_or_404(id=id, alive=True)

        destination_sheet = Sheet.objects.get_or_404(id=request.json['sheet']['id'])
        # save current details in history 
        event.history.append(event)
        event.sheet = destination_sheet
        event.updated_at = datetime.now()
        event.save()
      
        return jsonify(ok=True,objects=[event.to_json()]),200

    def delete(self, id):
        event = Event.objects.get_or_404(id=id,alive=True)
        event.alive=False
        event.updated_at = datetime.now()
        event.history.append( event )
        event.save()
        return jsonify(ok=True), 200