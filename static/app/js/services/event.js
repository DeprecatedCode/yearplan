angular.module('Event',['$resource','Sheet', function($resource, Sheet) {
    
    var Event = $resource('/sheet/:sheetId/event/:eventId',
                     {sheetId : '@sheet.id', eventId:'@id'},
                     {
                        'get' : {
                            url: '/event/:eventId',
                            method: 'GET'
                        },
                         'update' : {
                            url : '/event/:eventId',
                             method: 'GET'
                         }
                     }
                    );
    Event.prototype.query = function() {
        var params, success, error;
        params = arguments[0] || angular.noop;
        success = arguments[1] || angular.noop;
        error = arguments[2] || angular.noop; 
        
        return $http.get('/event/', params).then(success, error);
    };
}]);