'use strict';
angular.module('yearplan.controllers').
    controller('authentication',
    ['$scope', '$state', 'Auth',
        function ($scope, $state, Auth) {
            $scope.loggedIn = false;
            
            /* http://beletsky.net/2013/11/simple-authentication-in-angular-dot-js-app.html */
            $scope.login = function() {
                
                var success = function(data, status) {

                    if (!data.ok) return false;
                    
                    delete $scope.password;
                    
                    Auth.getUser(function(user){
                        $scope.loggedIn = true;
                        $scope.user = user;
                        // redirect to entry view
                        $state.go('sheets');
                    });
                    
                };
                
                var err = function (data, headers) {
                    //@Todo   
                };
                
                Auth.login($scope.email, $scope.password).success(success).error(err);
            }
            
            $scope.logout = function(){
                //@Todo
                console.log('Logging out...');
                
                Auth.logout(function(){
                   delete $scope.email;
                   delete $scope.user;
                   $scope.loggedIn = false;
                   $state.go('login');
                });
            }
            
            function init(){
            /** check if auth cookie is set 
             */
                Auth.getStatus(function(status){
                    $scope.loggedIn = status;
                    if(status){
                        Auth.getUser(function(user){
                            $scope.user = user;
                        });
                    }
                });
            }
        }
    ]);