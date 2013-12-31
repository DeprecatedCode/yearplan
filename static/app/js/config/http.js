/** Interceptor for handling auth (..redirects to login) **/
angular.module('yearplan').
config(function($httpProvider){
    $httpProvider.responseInterceptors.push(
      function ($q, $window, $location) {
        return function(promise) {
            
            var success = function(response) {
                return response;
            },
            error = function(response) {
                if(response.status === 401 || response.status === 500) {
                    $location.url('login');
                }
                return $q.reject(response);
            };
            
            return promise.then(success, error);
        }
    });
});
