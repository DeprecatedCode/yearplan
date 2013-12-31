/* User resource */
angular.module('yearplan.services').
factory('User', ['$http', 'yearplanTransformer', function ($http, transformer) {
    var path = '/user/';
    
    $http.defaults.transformResponse.push( transformer );
    
    var User = function(value){
        angular.copy(value || {}, this);
    };
    /**
     *   @returns a promise
     */
    User.prototype.register = function (data, callback) {
        
        return $http.post({
            url : this.path,
            method : 'POST',
            data : data
        }).then(callback);
    }
    
    User.prototype.save = function(data, callback) {
        // merge user with incoming data
        angular.extend(this, data);
        if (!'id' in this ) {
            throw new Error('id not set. Cannot perform operation')
        }
        
        return $http({
            url: [path,this.id].join(''),
            method: 'POST'
        }).then(callback);
    }
    
    User.get = function(data, callback){
        angular.extend(this, data);
        if (! 'id' in this ) {
            throw new Error('id not set. Cannot perform operation')
        }
        return $http({
            url : [path,this.id].join(''),
            method: 'GET',
            transformResponse : function(data, headers){
                var d = $.parseJSON(data);

                if( d.objects.length > 0) {
                    return d.objects[0];
                }
            }
        }).then(callback);
    }
    /**
     *  @param {Object} data parameters to send to the server
     *  @param {function} callback callback to handle the response
     *  
     *  returns a promise
     */
    User.query = function(){
        // {}, success, error 
        var data, success, error;
        
        switch( arguments.length ){
            case 1:
              if( angular.isFunction(arguments[0])) {
                  data = {};
                  success=arguments[0];
                  error=angular.noop;
              };
              break;
            case 2:
              data = arguments[0];
              success = angular.isFunction(arguments[1]) ? arguments[1] : angular.noop;
            case 3:
              error = angular.isFunction(arguments[2]) ? arguments[2] : angular.noop;
              break;
        };

        
        return $http({
            data : data,
            url : path,
            method : 'GET'
        }).error(error).then(success);
    }
   
    User.getFromSheet = function(params, callback) {
        var url = '/sheet/:sheetId/users';
        
        var sheetId = params.sheetId,
            userId = ('userId' in params ) ? params.userId : undefined;
            
        url = url.replace(':sheetId', params.sheetId);
        
        if (userId){
            url = [url, params.userId].join('/');
        }
        
        return $http({
            url : url,
            method : 'GET'
        }).then(callback);
    }

    return User;
}
]);

