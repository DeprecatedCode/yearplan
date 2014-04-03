'use strict';
angular.module('yearplan.services')
.factory('Event', ['$resource', function($resource) {
    return $resource('/sheet/:sheetId/event/:eventId',
                     {sheetId : '@sheet_id', eventId:'@id'},
                     {
                        'get' : {
                            url: '/event/:eventId',
                            method: 'GET'
                        },
                        'save' : {
                            url: '/sheet/:sheetId/event/',
                            method: 'POST',
                            params : {
                                sheetId : '@sheet_id'
                            }
                        },
                        'update' : {
                            url : '/event/:eventId',
                            method: 'PUT'
                        },
                        'query' : {isArray : false, method: 'GET'}
                     }
                    );
}]);