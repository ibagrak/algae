/* Author: @ibagrak */

$(document).ready( function() {
    
    $('#signup').on('hidden', function () {
        // restore form and buttons to original state
        var result = $(this).find('.form_result');
        var form = $(this).find('form');
        var btn = $('#signup_btn').removeClass('restore').addClass('submit');
        
        form.find(':input').removeAttr('disabled');
        form.find(':input').val('');
        form.validate().resetForm();
        
        btn.html('Sign up');
        btn.removeAttr('disabled');
        
        result.hide(); 
        form.show();
        btn.show();
    });
      
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
    
    $('.submit').live('click', function() {
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
            $('#signup_form').find(':input').attr('disabled', '');
            
            // Disable button
            var btn = $(this);
            btn.attr('disabled', '');
            btn.html('Sending...');
            
            $.ajax({
                type: 'GET',
                url: "/email-signup",
                data: kvs,
            }).done(function(data, code, jqxhr) {
                var data = $.parseJSON(data);
                var code = data['code'];
                var message = data['message'];
                
                if (code == 200) { // success
                    // hide form & show
                    btn.parents('.modal').find('.form_result').html('Success!');
                    btn.parents('.modal').find('form').hide();
                    btn.parents('.modal').find('.form_result').show();
                    
                    btn.hide();
                } else {
                    // should never happen (HTTP error code always matches JSON 'code')
                }
            }).fail(function(jqxhr, code, exception) {
                // TODO: Error handling
                var data = $.parseJSON(jqxhr.responseText);
                var code = data['code'];
                var message = data['message'];
                
                btn.parents('.modal').find('.form_result').html('So sorry! ' + message);
                btn.parents('.modal').find('form').hide();
                btn.parents('.modal').find('.form_result').show();
                
                btn.removeAttr('disabled');
                btn.html('Try again');
                btn.removeClass('submit').addClass('restore');
            }); 
        }
    });
    
    $('.restore').live('click', function() {
        $(this).removeClass('restore').addClass('submit');
        
        // enable form
        var result = $(this).parents('.modal').find('.form_result');
        var form = $(this).parents('.modal').find('form');
        form.find(':input').removeAttr('disabled');
        form.find(':input').val('');
        form.validate().resetForm();
        
        result.hide(); 
        form.show();
        $(this).html('Sign up')
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
