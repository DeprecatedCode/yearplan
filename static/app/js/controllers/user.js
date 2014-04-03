'use strict';
angular.module('yearplan.controllers').
    controller('registration', ['$scope', '$state', 'User',
        function ($scope, $state, User) {

            $scope.register = function () {
                var newUser = {
                    name: [$scope.firstname, $scope.lastname].join(' '),
                    email : $scope.email,
                    password : $scope.password,
                    alive: true,
                    location : $scope.location,
                    description :  $scope.description
                };

                User.create(newUser, function(data, headers){
                    $state.go('users');
                });

            };
        }
    ]).
    controller('userListCtrl',
    [        '$scope', '$stateParams', 'User',
    function( $scope , $stateParams, User) {

        User.query(function(resp){
            $scope.users = resp.data;
        });

    }]).
    controller('userDetailCtrl',
    [        '$scope', '$stateParams', 'User',
    function( $scope , $stateParams, User) {
        
        $scope.user = User.get({id:$stateParams.userId}, function(resp){
            $scope.user = resp.data;
        });
       // @Todo
    }]);