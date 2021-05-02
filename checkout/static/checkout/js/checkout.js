const caTaxLabel = $('#taxes-label');
const caTaxAmt = $('#taxes-amt');
const grandTotal = $("#gtotal-amt");
const caGrandTotal = $("#gtotal-amt-ca");
const shipState2 = ('#id_ship_state');

$(document).ready(function() {
    //MD Bootstrap payment stepper
    $('.stepper').mdbStepper();

    /* Add gray to SelectState when page loads and change when selected */
    /* if statement handles preload */
    if ($('#id_ship_city').val() != '' ) {
        $(shipState2).css('color', '#47646f');
    } else {
        $(shipState2).css('color', '#c3ccd3');
    }

    $(shipState2).on('change', function() {
        $(shipState2).css('color', '#47646f');
        if ($(shipState2).val() === "California") {
            $(caTaxLabel).removeClass("d-none");
            $(caTaxAmt).removeClass("d-none"); 
            $(caGrandTotal).removeClass("d-none");
            $(grandTotal).addClass("d-none");
            localStorage.setItem("ca", "true");
        }
    });

    $('#id_bill_state').css('color', '#c3ccd3');
    
    $('#id_bill_state').on('change', function() {
        $('#id_bill_state').css('color', '#47646f'); 
    });
});

