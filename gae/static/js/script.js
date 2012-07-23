/* Author: @ibagrak */

$(document).ready( function() {
    
    // modal popup can be in 2 states: hidden or shown
    // when shown: it can be in 3 states: 
    // 1. start state - form shown and validating input, button active
    // 2. submitting state - form deactivated, button deactivated (ajax request sent)
    // 3. submitted state - form deactivated, button deactivated, result message shown (ajax response received)
    // 
    //      if submitted state result is error we can (1) close modal or (2) restore to state 1.
    //      if submitted state result is success we can (1) close modal
    
    $('.tri-state').each(function () {
        var modal = $(this);
        var frm = $(this).find('form');
        var btn = $(this).find('.submit');
        var orig_btn_label = btn.html();
        var result = $(this).find('.form_result');
        var action = frm.attr('name');
        
        // restore state when modal is hidden
        modal.on('hidden', function () {    
            var result = $(this).find('.form_result');
                  
            frm.find(':input').removeAttr('disabled');
            frm.find(':input').val('');
            frm.validate().resetForm(); // reset validation state
            
            btn.removeClass('restore').addClass('submit');
            btn.html(orig_btn_label);
            btn.removeAttr('disabled');
            
            result.hide(); 
            frm.show();
            btn.show();
        });
          
        // submit button callback
        btn.live('click', function() {
            // restore form after error message
            if (btn.hasClass('restore')) {
                btn.removeClass('restore');
                
                // enable form  
                frm.find(':input').removeAttr('disabled');
                frm.find(':input').val('');
                frm.validate().resetForm();
                        
                result.hide(); 
                frm.show();
                $(this).html(orig_btn_label)
            // submit button normally
            } else {
                var kvs = {}
                if (frm.validate().form()) {
                    frm.find(":input").each(function() {
                        if ($(this).attr('type') == 'password') {
                            kvs[$(this).attr('id')] = MD5($(this).val());
                        } else {
                            kvs[$(this).attr('id')] = $(this).val();
                        }
                    });
                    
                    // Disable form
                    frm.find(':input').attr('disabled', '');
                    
                    // Disable button
                    btn.attr('disabled', '');
                    btn.html('Sending...');
                    
                    $.ajax({
                        type: 'GET',
                        url: '/' + action,
                        data: kvs,
                    }).done(function(data, code, jqxhr) {
                        var data = $.parseJSON(data);
                        var code = data['code'];
                        var message = data['message'];
                        
                        if (code == 200) { // success
                            // if we were trying to signin reload with new session on success
                            if (action == 'email-signin') {
                                location.reload();
                            } else {
                                // hide form & show result
                                result.html('Success!');
                                frm.hide();
                                result.show();
                                
                                btn.hide();
                            }
                        } else {
                            // should never happen (HTTP error code always matches JSON 'code')
                        }
                    }).fail(function(jqxhr, code, exception) {
                        // TODO: Error handling
                        var data = $.parseJSON(jqxhr.responseText);
                        var code = data['code'];
                        var message = data['message'];
                        
                        result.html('So sorry! ' + message);
                        frm.hide();
                        result.show();  
                        
                        btn.removeAttr('disabled');
                        btn.html('Try again');
                        btn.addClass('restore');
                    }); 
                }
            }  
        });
        
        // setup validation to play well with default Twitter bootstrap classes
        frm.validate({
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
    });
    
    $("#create").validate({
        errorClass:      "error",
        errorElement:    "span", 
        
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
    
    $("#create_btn").click(function() {
        var btn = $(this);
        var frm = $(this).parents('form');
        var result = $(this).siblings('.form_result');
        
        var kvs = {}
        if (frm.validate().form()) {
            frm.find(":input").each(function() {
                if ($(this).attr('type') == 'password') {
                    kvs[$(this).attr('id')] = MD5($(this).val());
                } else {
                    kvs[$(this).attr('id')] = $(this).val();
                }
            });
            
            // Disable form
            frm.find(':input').attr('disabled', '');
            
            // Disable button
            btn.attr('disabled', '');
            
            var kvs = JSON.stringify(kvs);
            
            $.ajax({
                type: 'PUT',
                url: '/rest/Widgets',
                data: kvs,
                dataType: "json",
                contentType: "application/json; charset=utf-8"
            }).done(function(data, code, jqxhr) {
                var code = data['code'];
                var message = data['message'];
                
                // Restore
                frm.find(':input').removeAttr('disabled');
                frm.find(':input').val('');
                btn.removeAttr('disabled');
                
                if (code == 200) { // success                   
                    var id = data['message']['id'];
                    
                    $.ajax({
                        type: 'GET',
                        url: '/rest/Widget/' + id,
                        dataType: "json",
                        contentType: "application/json; charset=utf-8"
                    }).done(function(data, code, jqxhr) {
                        var code = data['code'];
                        var message = data['message'];
                        
                        if (code == 200) {  
                            // hide form & show result
                            result.html('Success!');
                            result.show();
                            result.fadeOut('slow');
                            
                            $("#entity-row").tmpl([{id : data['message']['id'], obj : JSON.stringify(data['message'])}]).prependTo("#entities > tbody");
                        } else {
                            // should never happen (HTTP error code always matches JSON 'code')
                            result.html('Couldn\'t retrieve created entity!');
                            result.show();
                            result.fadeOut('slow');
                        }                  
                    }).fail(function(jqxhr, code, exception) {
                        // should never happen (HTTP error code always matches JSON 'code')
                        result.html('Couldn\'t retrieve created entity!');
                        result.show();
                        result.fadeOut('slow');
                    });
                } else {
                    // should never happen (HTTP error code always matches JSON 'code')
                    result.html('Error!');
                    result.show();
                    result.fadeOut('slow');
                }
            }).fail(function(jqxhr, code, exception) {
                // TODO: Error handling
                var data = $.parseJSON(jqxhr.responseText);
                var code = data['code'];
                var message = data['message'];
                
                // Restore
                frm.find(':input').removeAttr('disabled');
                frm.find(':input').val('');
                btn.removeAttr('disabled');
                
                result.html('So sorry! ' + message);
                result.show();  
            }); 
        }
    });
});
