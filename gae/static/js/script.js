/* Author: @ibagrak */

$(document).ready( function() {
    
    $('#signup_form').validate({
        errorClass:     "error",
        errorElement:   "span", // class='help-inline'
        highlight: function(element, errorClass, validClass) {
            if (element.type === 'radio') {
                this.findByName(element.name).parent("div").parent("div").removeClass(validClass).addClass(errorClass);
            } else {
                $(element).parent("div").parent("div").removeClass(validClass).addClass(errorClass);
            }
        },
        unhighlight: function(element, errorClass, validClass) {
            if (element.type === 'radio') {
                this.findByName(element.name).parent("div").parent("div").removeClass(errorClass).addClass(validClass);
            } else {
                $(element).parent("div").parent("div").removeClass(errorClass).addClass(validClass);
            }
        }
    });
    
    $('#signup_btn').click(function() {
        var kvs = {}
        if ($('#signup_form').validate().form()) {
            $('#signup_form').find(":input").each(function() {
                if ($(this).attr('type') == 'password') {
                    kvs[$(this).attr('id')] = MD5($(this).val())
                } else {
                    kvs[$(this).attr('id')] = $(this).val()
                }
            });
            
            // Disable form
            
            // Disable button
            
            $.ajax({
                type: 'GET',
                url: "/email-signup",
                data: kvs,
            }).done(function(data, code, jqxhr) {
                var code = data['code'];
                var message = data['message'];
                
                if (code == 200) { // success
                    // hide form & show 
                } else {
                    
                }
            }).fail(function(jqxhr, code, exception) {
                // TODO: Error handling
                
            }); 
        }
    });
    
    
    
//    $.ajax({
//        type: 'POST',
//        url: "/api/v1/pitch" + window.location.pathname,
//        data: kvs,
//        dataType: "json",
//        contentType: "application/json; charset=utf-8"
//    }).done(function(data, code, jqxhr) {
//        var code = data['code'];
//        var message = data['message'];
//        var feedback; 
//        
//        if (code == PARTIALLY_SAVED || code == SAVED) {
//            feedback = 'All changes saved<span id="saved_ago"></span>.'
//        } else {
//            feedback = 'An unknown error has occured.'
//        }
//        
//        if ($('.input-overflown').length > 0) {
//            feedback = feedback + ' Be sure to correct other fields.';
//        }
//        
//        $('.word_limited, .char_limited').removeClass('input-changed');
//        setTimeout(function() {$('#form_status').html(feedback);}, 400);
//        
//    }).fail(function(jqxhr, code, exception) {
//        // TODO: Error handling
//        $('#form_status').html('A ' + jqxhr.status + ' error occured while saving.');
//    });
});
