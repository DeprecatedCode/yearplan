'use strict';
angular.module('yearplan.controllers').
    controller('EventsController',
    [        '$scope', '$state', 'Event',
    function( $scope , $state, Event) {
       // @Todo
        $scope.event = {};
        
        function loadSheetEvents (sheetId) {
            Event.query({sheetId : sheetId},function(resp){
                $scope.events = resp.objects;
            });
        };
        
        function loadEvent (eventId) {
            
        }
        
        if( $state.params.sheetId ) {
            loadSheetEvents( $state.params.sheetId);
            $scope.event = {
                sheet_id : $state.params.sheetId
            };
        }
        
        $scope.saveEvent = function() {
            // @todo Check for valid sheet Id
            var event = new Event($scope.event);
            event.$save();
            $state.go('sheets.detail.events', {sheetId: $state.params.sheetId});
        }
        
        
        
       
    }]);