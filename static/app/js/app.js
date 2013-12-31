'use strict';

angular.module('yearplan.services', ['ngCookies', 'ngResource']);

angular.module('yearplan.controllers', ['yearplan.services']);

angular.module('yearplan', [
    'ui.router', 'yearplan.controllers', 'yearplan.services'
]).
run(
    ['$rootScope', '$state', '$stateParams', 'api',
    function ($rootScope,   $state,   $stateParams, api) {
    // It's very handy to add references to $state and $stateParams to 
    // the $rootScope so that you can access them from any scope within 
    // your applications.For example,
    //   <li ng-class="{ active: $state.includes('contacts.list') }"> 
    // will set the <li>
    // to active whenever 'contacts.list' or one of its decendents is active.
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        api.initialize({token: false});
    }
]);