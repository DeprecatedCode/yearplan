/**
 * @package Yearplan
 * @subpackage  Services
 * @name  Sheet
 * */
angular.module('yearplan.services').
factory('Sheet',['$resource','$http',
    function($resource, $http) {
        return $resource('/sheet/:sheetId',{ sheetId : '@id' },
            {
                
                trash : {
                    url : '/sheet/trash',
                    method : 'GET'
                },
                query : {isArray : false, method: 'GET'}
               
            }
        );
    }
]);