'use strict';
angular.module('yearplan.controllers').
    controller('SheetsController',
    [        '$scope', 'Sheet', '$state',
    function( $scope , Sheet, $state) {
       
        $scope.sheet = {};
        $scope.save = function(){
            //$scope.sheets.push( $scope.sheet );
            /**
             * @todo Send data to actual server 
             *
             */
            var sheet = new Sheet($scope.sheet);
            sheet.$save(
              function(resp){
                var sh = resp.objects.pop();
                $state.go('sheets.detail', sh.id)
            });
        }
        
        $scope.remove = function(aSheet) {
            $scope.slice(aSheet);
            
            /**
             *  @todo dispatch an HTTP request to remove the sheet
             */
        }

        function init(sheetId) {
            var sheet = new Sheet({id: sheetId});
            
            sheet.$get(function(resp){
                $scope.sheet = resp.objects[0];
            });
            $state.go('sheets.detail.events');
        }
        
        if ( $state.params.sheetId ) {
            init($state.params.sheetId);
        }
        
        // get the sheets
        Sheet.query(function(resp){
                $scope.sheets = resp.objects;
        });
        
    }]);
    