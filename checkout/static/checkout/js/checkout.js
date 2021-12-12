const shippingForm = document.getElementById('shipping-form');
const shipFullName = $('#id_ship_full_name');
const shipStreet1 = $('#id_ship_street_address1');
const shipStreet2 = $('#id_ship_street_address2');
const shipCity =  $('#id_ship_city');
const shipState =  $('#id_ship_state');
const shipZipCode = $('#id_ship_zipcode');
const shipPhone = $('#id_ship_phone_number');
const billFullName = $('#id_bill_full_name');
const billStreet1 = $('#id_bill_street_address1');
const billStreet2 = $('#id_bill_street_address2');
const billCity = $('#id_bill_city');
const billState = $('#id_bill_state');
const billZipCode = $('#id_bill_zipcode');
const billPhone = $('#id_bill_phone_number');

    
$(document).ready(function() {
    //MD Bootstrap payment stepper
    $('.stepper').mdbStepper();

    /* If CA, set cookie secure, https://javascript.info/cookie */
    function getCaShipTax() {
        if ($(shipState).val() === "CA") {
            document.cookie = "ca=true; secure";
        } else {
            document.cookie = "ca=false; secure";
        }
    }

    /* Add gray to SelectState when page loads and change when selected */
    /* if statement handles preload */
    if ($(shipCity).val() != '' ) {
        $(shipState).css('color', '#47646f');
    } else {
        $(shipState).css('color', '#c3ccd3');
    }

    /* When state input changes, change font color */
    $(shipState).on('change', function() {
        $(shipState).css('color', '#47646f');
    });

    $(billState).css('color', '#c3ccd3');
    
    $(billState).on('change', function() {
        $(billState).css('color', '#47646f'); 
    });

    /* If CA value preloaded as shipping addresss */
    if ($(shipState).val() === "CA") {
        getCaShipTax();
    }

    /* if ca entered as shipping state */
    $(shipState).on('change', function() {
        getCaShipTax();
    });

    /* Load shipping address to billing address when requested */
    $('input[name=same-as-ship]:checkbox').change(function() {
        if ($(this).is(':checked')) {
            billFullName.val(shipFullName.val());
            billStreet1.val(shipStreet1.val());
            billStreet2.val(shipStreet2.val());
            billCity.val(shipCity.val());
            billState.val(shipState.val());
            $(billState).css('color', '#47646f'); 
            billZipCode.val(shipZipCode.val());
            billPhone.val(shipPhone.val());
        } else {
            billFullName.val("");
            billStreet1.val("");
            billStreet2.val("");
            billCity.val("");
            billState.val("");
            billZipCode.val("");
            billPhone.val("");
        }
    });
    //Post to checkout view to load order form
    if(shippingForm) {

        shippingForm.addEventListener('submit', function(ev) {
            ev.preventDefault();
            $('#submit-ship-button').attr('disabled', true);
            $('#shipping-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
        
        
            // From using {% csrf_token %} in the form
            let csrfToken2 = $('input[name="csrfmiddlewaretoken"]').val();
            let fedexFullName = $('#id_ship_full_name').val();
            let fedexEmail = $('#id_email').val();
            let fedexCompName = $('#id_ship_comp_name').val();
            let fedexPhoneNumber = $('#id-ship_phone_number').val();
            let fedexStreetAddress1 = $('#id_ship_street_address1').val();
            let fedexStreetAddress2 = $('#id_ship_street_address2').val();
            let fedexCity = $('#id_ship_city').val();
            let fedexState = $('#id_ship_state').val();
            let fedexZipCode = $('#id_ship_code').val();


            let postData2 = {
                'csrfmiddlewaretoken': csrfToken2,
                'ship_full_name': fedexFullName, 
                'email': fedexEmail, 
                'ship_comp_name': fedexCompName,
                'ship_phone_number': fedexPhoneNumber, 
                'ship_street_address1': fedexStreetAddress1,
                'ship_street_address2': fedexStreetAddress2,
                'ship_city': fedexCity, 
                'ship_state': fedexState,
                'ship_zipcode': fedexZipCode,
                'action': "fedex_address"
            }
            var url = '/checkout/payment/';

            //$.post(url, postData2, function(data, status) {
            //    console.log(`${data} and status is ${status}`);
            //}); 
        }); 
    }
});
