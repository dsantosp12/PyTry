/**
 * Created by dsantos on 7/21/15.
 */
$(document).ready(function(){
    //MATERIALIZE

    $('select').material_select();

    $('.button-collapse').sideNav();

    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 2 // Creates a dropdown of 15 years to control year
    });

    var doc = new jsPDF();

// We'll make our own renderer to skip this editor
var specialElementHandlers = {
	'#editor': function(element, renderer){
		return true;
	}
};

// All units are in the set measurement for the document
// This can be changed to "pt" (points), "mm" (Default), "cm", "in"
doc.fromHTML($('.printable').get(0), 15, 15, {
	'width': 170,
	'elementHandlers': specialElementHandlers
});

});