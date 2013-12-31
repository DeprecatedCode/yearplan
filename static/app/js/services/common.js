/**
 * @package Yearplan 
 * @subpackage  Services
 * @name Common
 * 
 * @description Common services that are used by the other services...
 * */
angular.module('yearplan.services').value('yearplanTransformer', 
    function(data, headers){
        //var r = $.parseJSON(data);
        return data.objects;
});