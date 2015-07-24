/**
 * Created by dsantos on 7/21/15.
 */
$(document).ready(function() {
    //MATERIALIZE

    $('select').material_select();

    $('.button-collapse').sideNav();

    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 2 // Creates a dropdown of 15 years to control year
    });

});
