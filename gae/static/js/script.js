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
    
    var make_ajax_form = function (type, done_func) {
        var btn_selector = '#' + type + '_btn';

        $('#' + type + '_btn').click(function() {
            if (type == 'create') {
                var URL = '/rest/Widgets'; 
                var t = 'PUT';
            } else if (type == 'update') {
                var id = $(btn_selector).data('id');
                var URL = '/rest/Widget/' + id;
                var t = 'POST';
            }

            var btn = $(this);
            var frm = $(this).parents('form');
            var result = $(this).siblings('.form_result');
            
            var restore = function() {
                // Restore
                // only restore children inputs of controls or checkboxes (doesn't apply to datepicker)
                frm.find('.controls > :input').removeAttr('disabled');
                frm.find('.controls > :input').val('');
                frm.find('.checkbox > :input').removeAttr('disabled');
                btn.removeAttr('disabled');
            };
            
            var show_result = function() {
                // hide form & show result
                result.html('Success!');
                result.show();
                result.fadeOut('slow');
            };
            
            $(frm).validate({
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
                    type: t,
                    url: URL,
                    data: kvs,
                    dataType: "json",
                    processData: false,
                    contentType: "application/json; charset=utf-8"
                }).done(function(data, code, jqxhr) {
                    // Restore
                    restore();
                    
                    if (done_func) {
                        done_func(data, show_result);
                    }
                    
                }).fail(function(jqxhr, code, exception) {
                    // TODO: Error handling
                    var data = $.parseJSON(jqxhr.responseText);
                    var code = data['code'];
                    var message = data['message'];
                    
                    // Restore
                    restore();
                    
                    result.html('So sorry! ' + message);
                    result.show();  
                }); 
            }
        });
    }
    
    // if PUT API call is successful, we want to retrieve the new item and place it in the table below
    // this function is a parameter to make_ajax_form()
    var done_create_func = function (data, show_result) {
        var code = data['code'];
        var message = data['message'];
                    
        if (code == 200) { // success                   
            var id = message['id'];
            
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
                    show_result('Success!');
                    
                    $("#entity-row").tmpl([{id : data['message']['id'], obj : JSON.stringify(data['message'])}]).prependTo("#entities > tbody");
                } else {
                    // should never happen (HTTP error code always matches JSON 'code')
                    show_result('Couldn\'t retrieve created entity!');
                }                  
            }).fail(function(jqxhr, code, exception) {
                // should never happen (HTTP error code always matches JSON 'code')
                show_result('Couldn\'t retrieve created entity!');
            });
        } else {
            // should never happen (HTTP error code always matches JSON 'code')
            show_result('Error!');
        }                
    }

    // if POST API call is successful, we want to update the item summary in the table
    // this function is a parameter to make_ajax_form()
    var done_update_func = function (data, show_result) {
        var code = data['code'];
        var message = data['message'];
                    
        if (code == 200) { // success                   
            var id = message['id'];
            
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
                    show_result('Success!');
                    
                    // FIXME: wonky
                    var btn_selector = '.update_btn[data-id=\"' + id + '\"]';
                    var btn = $(btn_selector);
                    var summary_cell = btn.parents('tr').find('td:nth-child(2)');
                    
                    btn.removeAttr('disabled');   
                    summary_cell.html(JSON.stringify(message));
                } else {
                    // should never happen (HTTP error code always matches JSON 'code')
                    show_result('Couldn\'t retrieve updated entity!');
                }                  
            }).fail(function(jqxhr, code, exception) {
                // should never happen (HTTP error code always matches JSON 'code')
                show_result('Couldn\'t retrieve updated entity!');
            });
        } else {
            // should never happen (HTTP error code always matches JSON 'code')
            show_result('Error!');
        }

        // after update is submitted, the button becomes disabled again until next row is selected
        $('#update_btn').attr('disabled', '');
        $('#update_btn').addClass('disabled');
    }

    make_ajax_form('create', done_create_func); 
    make_ajax_form('update', done_update_func);
    
    $('.update_btn').live('click', function() {     
        var update_form = $('#update_form');
        var btn = $(this);

        
        // toggle other update buttons
        $('.update_btn').each(function() {
            $(this).removeAttr('disabled');
        });

        // disable update buttons (the one clicked and form button below)
        $(this).attr('disabled', '');
        $('#update_btn').attr('disabled', '');
        $('#update_btn').addClass('disabled');

        $.ajax({
                type: 'GET',
                url: '/rest/Widget/' + $(this).attr('data-id'),
                dataType: "json",
                contentType: "application/json; charset=utf-8"
         }).done(function(data, code, jqxhr) {
            var code = data['code'];
            var message = data['message'];
                        
            if (code == 200) {
                //load the form with item to update
                $.each(message, function(key, value) {
                    var input = update_form.find('#' + key);
                    if (input.parent().hasClass('datepicker')) {
                        var parent = input.parent();
                        parent.data('date', value);
                        parent.datepicker('update');
                    } 

                    input.attr('value', value);
                    input.val(value);
                });

                $('#update_btn').removeAttr('disabled');
                $('#update_btn').removeClass('disabled');
                $('#update_btn').data('id', btn.data('id')); // assign widget id for updating
            } else {
                // should never happen (HTTP error code always matches JSON 'code')
                var summary_cell = btn.parents('tr').find('td:nth-child(2)');
                var summary = summary_cell.html();

                summary_cell.html(message).delay().fadeOut(slow, function () {
                    summary_cell.html(summary);
                });

                $(this).removeAttr('disabled');
            }
        }).fail(function(jqxhr, code, exception) {
            // should never happen (HTTP error code always matches JSON 'code')
            // TODO: Error handling
            var data = $.parseJSON(jqxhr.responseText);
            var code = data['code'];
            var message = data['message'];

            var summary_cell = btn.parents('tr').find('td:nth-child(2)');
            var summary = summary_cell.html();

            summary_cell.html(message).delay().fadeOut(slow, function () {
                summary_cell.html(summary);
            });

            $(this).removeAttr('disabled');
        });
    });
    
    $('.delete_btn').live('click', function() {
        var btn = $(this);

        //delete item
        $.ajax({
                type: 'DELETE',
                url: '/rest/Widget/' + $(this).attr('data-id'),
                dataType: "json",
                contentType: "application/json; charset=utf-8"
         }).done(function(data, code, jqxhr) {
            var code = data['code'];
            var message = data['message'];
                        
            if (code == 200) {
                btn.parents('tr').remove();
            } else {
                // should never happen (HTTP error code always matches JSON 'code')
                var summary_cell = btn.parents('tr').find('td:nth-child(2)');
                var summary = summary_cell.html();

                summary_cell.html(message).delay().fadeOut(slow, function () {
                    summary_cell.html(summary);
                });
            }                  
        }).fail(function(jqxhr, code, exception) {
            // should never happen (HTTP error code always matches JSON 'code')
            var data = $.parseJSON(jqxhr.responseText);
            var code = data['code'];
            var message = data['message'];

            var summary_cell = btn.parents('tr').find('td:nth-child(2)');
            var summary = summary_cell.html();

            summary_cell.html(message).delay().fadeOut(slow, function () {
                summary_cell.html(summary);
            });
        });
    });

    $('div[id$="datepicker"]').datepicker();

    $('#tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
});
