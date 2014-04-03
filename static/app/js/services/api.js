/*
 * */
angular.module('yearplan.services').factory('api', function ($http, $cookies) {
    return {

        initialize : function(data){
            
            $http.defaults.headers.common['X-yearplan-user'] = data.token || $cookies.yearplan_user;
        },
        terminate : function(callback){
            
            delete $cookies.yearplan_user;
            delete $http.defaults.headers.common['X-yearplan-user'];
            if(angular.isFunction(callback)) callback();
        }
    };
});