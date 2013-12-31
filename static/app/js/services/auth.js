/**
 * @package  Yearplan
 * @subpackage  Services
 * @name Auth
 * 
 * @todo
 * 1.  
 */
angular.module('yearplan.services').
    factory('Auth', ['$http','$cookieStore','api', function ($http, $cookieStore, api) {
        var path = '/auth/';
        
        var Auth = function() {
            
        };
        
        Auth.login = function(email, password){
            
            return $http({
                url: '/auth/',
                method: 'POST',
                data : {email: email, password : password},
            }).success(function(data,status, headers){
                var token =  headers('X-yearplan-user');
                $cookieStore.put('token', token);
                api.initialize({token : token});
            });
        }
        
        Auth.getUser = function(callback){  
            if('user' in Auth && Auth.user ){
                callback(Auth.user);
                return true;
            }
            
            $http.get('/user/profile').success(function(data, status, headers){
                
                if ('objects' in data) {
                    var user = data.objects.shift();
                    Auth.user = user;
                    
                    callback(Auth.user);
                }
            });
        }
        
        Auth.getStatus = function(callback) {
            
            if (!$cookieStore.get('token'))
                callback({status:false});
                
            $http({
                url: '/auth/',
                method: 'GET',
                headers: {
                    'X-yearplan-user' : $cookieStore.get('token')
                }
            }).then(function(data){
                callback({status: data.ok});
            })
        }
        
        Auth.logout = function(cb){
            
            $http.delete('/auth/');
            
            api.terminate(function(){
                console.log('logged out');
            });
            
            cb();
        }
        
        return Auth;
    }
    ]);