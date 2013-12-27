# -*- coding utf-8 -*-
import os
from flask import render_template, make_response, send_from_directory
from flask.ext.classy import FlaskView, route

class AppView (FlaskView):

    def index (self):
        return render_template('index.html')
    
    #@route('/<path:path_item>', methods=['GET'])
    #def resources(self, path_item):
    #    from yearplan import application        
    #    return send_from_directory(
    #                os.path.join(
    #                    application.root_path,
    #                    application.static_folder
    #                ),
    #                path_item
    #    )
    #@route('/app/partials/<path:name>.html')
    #def partials(self, partial):
    #    return make_response(open('static/app/partials/%s.html' % partial).read())