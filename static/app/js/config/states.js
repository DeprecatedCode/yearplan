'use strict';
/* setup the states, using angular ui-router */
angular.module('yearplan').
  config(['$stateProvider', '$urlRouterProvider',
    function ($stateProvider, $urlRouterProvider) {
        
        $urlRouterProvider.when('/login','/' ).
            otherwise('/home');
        
        $stateProvider.state('auth', {
            url : '/',
            templateUrl : 'partials/login.html',
            controller: 'authentication'
        }).
        state('register', {
            url: '/register',
            templateUrl: 'partials/register.html',
            controller: 'registration'
        }).
        state('home', {
            url: '/',
            templateUrl: 'partials/home.html'
        }).
        state('sheets', {
            url : '/sheets',
            templateUrl: 'partials/sheets.list.html',
            controller : 'sheetListCtrl'
        }).
        state('sheets.create', {
            url : '/create',
            parent: 'sheets',
            templateUrl : 'partials/sheets.edit.html'
        }).
        state('sheets.detail', {
            url : '/{sheetId:[a-f0-9]*}',
            parent: 'sheets',
            templateUrl : 'partials/sheets.detail.html',
            controller : 'sheetDetailCtrl'
        }).
        state('users', {
            url : '/users',
            templateUrl: 'partials/users.list.html',
            controller : 'userListCtrl'
        }).
        state('users.detail', {
            url : '/{userId:[a-f0-9]*}',
            parent: 'users',
            templateUrl : 'partials/users.detail.html',
            controller: 'userDetailCtrl'
        }).
        state('sheets.events', {
            url : '/events',
            parent: 'sheets.detail',
            templateUrl : 'partials/events.list.html',
            controller : 'eventListCtrl'
        }).
        state('sheets.events.create', {
            url : '/create',
            templateUrl : 'partials/events.edit.html',
            controller : 'eventListCtrl'
        }).
        state('sheets.events.detail', {
            url : '/:sheetId/events/:eventId',
            parent : 'sheets',
            templateUrl: 'partials/events.detail.html',
            controller: 'eventDetailCtrl'
        });
    }]);
    
 