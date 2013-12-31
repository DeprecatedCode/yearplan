'use strict';
angular.module('yearplan.controllers').
    controller('sheetListCtrl',
    [        '$scope', 'Sheet',
    function( $scope , Sheet) {
        var path = '/sheet/';
        
        $scope.sheets = Sheet.query(function(resp){
            $scope.sheets = resp.objects;
        });
        
        $scope.create = function(){
            
            var sheet = new Sheet($scope.sheet);
            
            sheet.$save();
        }
        
        
    }])
    .controller('sheetDetailCtrl',
    [        '$scope', '$stateParams', 'Sheet',
    function( $scope , $stateParams, Sheet) {
        // @Todo
        $scope.create = function(){
        
            var sheet = new Sheet($scope.sheet);
            
            sheet.$save();
        }
        
        function init(sheetId) {
            var sheet = new Sheet({id: sheetId});
            
            sheet.$get(function(resp){
                console.log(resp);
                $scope.sheet = resp;
            });
        }
        
        
        init($stateParams.sheetId);
        
        
        
    }]);
    