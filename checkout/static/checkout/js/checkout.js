$(document).ready(function() {
    //MD Bootstrap payment stepper
    $('.stepper').mdbStepper();

    /* Add gray to SelectState when page loads and change when selected */
    /* if statement handles preload */
    if ($('#id_ship_city').val() != '' ) {
        $('#id_ship_state').css('color', '#47646f');
    } else {
        $('#id_ship_state').css('color', '#c3ccd3');
    }

    $('#id_ship_state').on('change', function() {
        $('#id_ship_state').css('color', '#47646f');
        if ($('#id_ship_state').val() === "CA") {
            $('#taxes-label').removeClass("d-none");
            $('#taxes-amt').removeClass("d-none"); 
            $("#gtotal-amt-ca").removeClass("d-none");
            $("#gtotal-amt").addClass("d-none");
            document.cookie = "ca=true";
        }
    });

    $('#id_bill_state').css('color', '#c3ccd3');
    
    $('#id_bill_state').on('change', function() {
        $('#id_bill_state').css('color', '#47646f'); 
    });
});

