'use strict';
/* setup the states, using angular ui-router */
angular.module('yearplan').
  config(['$stateProvider', '$urlRouterProvider',
    function ($stateProvider, $urlRouterProvider) {
        
        $urlRouterProvider.otherwise('/');
        
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
            url: '/home',
            templateUrl: 'partials/home.html'
        }).
        state('sheets', {
            url : '/sheets',
            templateUrl: 'partials/sheets.list.html',
            controller : 'SheetsController'
        }).
        state('sheets.create', {
            url : '/create',
            templateUrl : 'partials/sheets.edit.html'
        }).
        state('sheets.detail', {
            url : '/{sheetId:[a-f0-9]*}',
            controller : 'SheetsController',
            templateUrl : 'partials/sheets.detail.html',
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
        state('users.sheets', {
            templateUrl : 'partials/users.detail.html',
            controller: 'SheetListCtrl'
        }).
        state('sheets.detail.events', {
            //url : '/events',
            templateUrl : 'partials/events.list.html',
            controller : 'EventsController'
        }).
        state('sheets.detail.events.create', {
            url : '/create',
            templateUrl : 'partials/events.edit.html',
            controller : 'EventsController'
        }).
        state('sheets.detail.events.detail', {
            url : '/events/:eventId',
            parent : 'sheets',
            templateUrl: 'partials/events.detail.html',
            controller: 'EventsController'
        });
    }]);
    
 