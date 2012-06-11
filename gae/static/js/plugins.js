// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/

window.log = function f() {
    log.history = log.history || [];
    log.history.push(arguments);
    if (this.console) {
        var args = arguments;
        var newarr;

        try {
            args.callee = f.caller;
        } catch(e) {

        }

        newarr = [].slice.call(args);

        if (typeof console.log === 'object') {
            log.apply.call(console.log, console, newarr);
        } else {
            console.log.apply(console, newarr);
        }
    }
};

// make it safe to use console.log always

(function(a) {
    function b() {}
    var c = "assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn";
    var d;
    for (c = c.split(","); !!(d = c.pop());) {
        a[d] = a[d] || b;
    }
})(function() {
    try {
        console.log();
        return window.console;
    } catch(a) {
        return (window.console = {});
    }
}());

// place any jQuery/helper plugins in here, instead of separate, slower script files.
/* =========================================================
 * bootstrap-modal.js v2.0.4
 * http://twitter.github.com/bootstrap/javascript.html#modals
 * =========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================= */


!function ($) {

  "use strict"; // jshint ;_;


 /* MODAL CLASS DEFINITION
  * ====================== */

  var Modal = function (content, options) {
    this.options = options
    this.$element = $(content)
      .delegate('[data-dismiss="modal"]', 'click.dismiss.modal', $.proxy(this.hide, this))
  }

  Modal.prototype = {

      constructor: Modal

    , toggle: function () {
        return this[!this.isShown ? 'show' : 'hide']()
      }

    , show: function () {
        var that = this
          , e = $.Event('show')

        this.$element.trigger(e)

        if (this.isShown || e.isDefaultPrevented()) return

        $('body').addClass('modal-open')

        this.isShown = true

        escape.call(this)
        backdrop.call(this, function () {
          var transition = $.support.transition && that.$element.hasClass('fade')

          if (!that.$element.parent().length) {
            that.$element.appendTo(document.body) //don't move modals dom position
          }

          that.$element
            .show()

          if (transition) {
            that.$element[0].offsetWidth // force reflow
          }

          that.$element.addClass('in')

          transition ?
            that.$element.one($.support.transition.end, function () { that.$element.trigger('shown') }) :
            that.$element.trigger('shown')

        })
      }

    , hide: function (e) {
        e && e.preventDefault()

        var that = this

        e = $.Event('hide')

        this.$element.trigger(e)

        if (!this.isShown || e.isDefaultPrevented()) return

        this.isShown = false

        $('body').removeClass('modal-open')

        escape.call(this)

        this.$element.removeClass('in')

        $.support.transition && this.$element.hasClass('fade') ?
          hideWithTransition.call(this) :
          hideModal.call(this)
      }

  }


 /* MODAL PRIVATE METHODS
  * ===================== */

  function hideWithTransition() {
    var that = this
      , timeout = setTimeout(function () {
          that.$element.off($.support.transition.end)
          hideModal.call(that)
        }, 500)

    this.$element.one($.support.transition.end, function () {
      clearTimeout(timeout)
      hideModal.call(that)
    })
  }

  function hideModal(that) {
    this.$element
      .hide()
      .trigger('hidden')

    backdrop.call(this)
  }

  function backdrop(callback) {
    var that = this
      , animate = this.$element.hasClass('fade') ? 'fade' : ''

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate

      this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
        .appendTo(document.body)

      if (this.options.backdrop != 'static') {
        this.$backdrop.click($.proxy(this.hide, this))
      }

      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

      this.$backdrop.addClass('in')

      doAnimate ?
        this.$backdrop.one($.support.transition.end, callback) :
        callback()

    } else if (!this.isShown && this.$backdrop) {
      this.$backdrop.removeClass('in')

      $.support.transition && this.$element.hasClass('fade')?
        this.$backdrop.one($.support.transition.end, $.proxy(removeBackdrop, this)) :
        removeBackdrop.call(this)

    } else if (callback) {
      callback()
    }
  }

  function removeBackdrop() {
    this.$backdrop.remove()
    this.$backdrop = null
  }

  function escape() {
    var that = this
    if (this.isShown && this.options.keyboard) {
      $(document).on('keyup.dismiss.modal', function ( e ) {
        e.which == 27 && that.hide()
      })
    } else if (!this.isShown) {
      $(document).off('keyup.dismiss.modal')
    }
  }


 /* MODAL PLUGIN DEFINITION
  * ======================= */

  $.fn.modal = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('modal')
        , options = $.extend({}, $.fn.modal.defaults, $this.data(), typeof option == 'object' && option)
      if (!data) $this.data('modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option]()
      else if (options.show) data.show()
    })
  }

  $.fn.modal.defaults = {
      backdrop: true
    , keyboard: true
    , show: true
  }

  $.fn.modal.Constructor = Modal


 /* MODAL DATA-API
  * ============== */

  $(function () {
    $('body').on('click.modal.data-api', '[data-toggle="modal"]', function ( e ) {
      var $this = $(this), href
        , $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
        , option = $target.data('modal') ? 'toggle' : $.extend({}, $target.data(), $this.data())

      e.preventDefault()
      $target.modal(option)
    })
  })

}(window.jQuery);

/**
 * jQuery Validation Plugin 1.9.0
 *
 * http://bassistance.de/jquery-plugins/jquery-plugin-validation/
 * http://docs.jquery.com/Plugins/Validation
 *
 * Copyright (c) 2006 - 2011 Jšrn Zaefferer
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */

(function($) {

$.extend($.fn, {
    // http://docs.jquery.com/Plugins/Validation/validate
    validate: function( options ) {

        // if nothing is selected, return nothing; can't chain anyway
        if (!this.length) {
            options && options.debug && window.console && console.warn( "nothing selected, can't validate, returning nothing" );
            return;
        }

        // check if a validator for this form was already created
        var validator = $.data(this[0], 'validator');
        if ( validator ) {
            return validator;
        }

        // Add novalidate tag if HTML5.
        this.attr('novalidate', 'novalidate');

        validator = new $.validator( options, this[0] );
        $.data(this[0], 'validator', validator);

        if ( validator.settings.onsubmit ) {

            var inputsAndButtons = this.find("input, button");

            // allow suppresing validation by adding a cancel class to the submit button
            inputsAndButtons.filter(".cancel").click(function () {
                validator.cancelSubmit = true;
            });

            // when a submitHandler is used, capture the submitting button
            if (validator.settings.submitHandler) {
                inputsAndButtons.filter(":submit").click(function () {
                    validator.submitButton = this;
                });
            }

            // validate the form on submit
            this.submit( function( event ) {
                if ( validator.settings.debug )
                    // prevent form submit to be able to see console output
                    event.preventDefault();

                function handle() {
                    if ( validator.settings.submitHandler ) {
                        if (validator.submitButton) {
                            // insert a hidden input as a replacement for the missing submit button
                            var hidden = $("<input type='hidden'/>").attr("name", validator.submitButton.name).val(validator.submitButton.value).appendTo(validator.currentForm);
                        }
                        validator.settings.submitHandler.call( validator, validator.currentForm );
                        if (validator.submitButton) {
                            // and clean up afterwards; thanks to no-block-scope, hidden can be referenced
                            hidden.remove();
                        }
                        return false;
                    }
                    return true;
                }

                // prevent submit for invalid forms or custom submit handlers
                if ( validator.cancelSubmit ) {
                    validator.cancelSubmit = false;
                    return handle();
                }
                if ( validator.form() ) {
                    if ( validator.pendingRequest ) {
                        validator.formSubmitted = true;
                        return false;
                    }
                    return handle();
                } else {
                    validator.focusInvalid();
                    return false;
                }
            });
        }

        return validator;
    },
    // http://docs.jquery.com/Plugins/Validation/valid
    valid: function() {
        if ( $(this[0]).is('form')) {
            return this.validate().form();
        } else {
            var valid = true;
            var validator = $(this[0].form).validate();
            this.each(function() {
                valid &= validator.element(this);
            });
            return valid;
        }
    },
    // attributes: space seperated list of attributes to retrieve and remove
    removeAttrs: function(attributes) {
        var result = {},
            $element = this;
        $.each(attributes.split(/\s/), function(index, value) {
            result[value] = $element.attr(value);
            $element.removeAttr(value);
        });
        return result;
    },
    // http://docs.jquery.com/Plugins/Validation/rules
    rules: function(command, argument) {
        var element = this[0];

        if (command) {
            var settings = $.data(element.form, 'validator').settings;
            var staticRules = settings.rules;
            var existingRules = $.validator.staticRules(element);
            switch(command) {
            case "add":
                $.extend(existingRules, $.validator.normalizeRule(argument));
                staticRules[element.name] = existingRules;
                if (argument.messages)
                    settings.messages[element.name] = $.extend( settings.messages[element.name], argument.messages );
                break;
            case "remove":
                if (!argument) {
                    delete staticRules[element.name];
                    return existingRules;
                }
                var filtered = {};
                $.each(argument.split(/\s/), function(index, method) {
                    filtered[method] = existingRules[method];
                    delete existingRules[method];
                });
                return filtered;
            }
        }

        var data = $.validator.normalizeRules(
        $.extend(
            {},
            $.validator.metadataRules(element),
            $.validator.classRules(element),
            $.validator.attributeRules(element),
            $.validator.staticRules(element)
        ), element);

        // make sure required is at front
        if (data.required) {
            var param = data.required;
            delete data.required;
            data = $.extend({required: param}, data);
        }

        return data;
    }
});

// Custom selectors
$.extend($.expr[":"], {
    // http://docs.jquery.com/Plugins/Validation/blank
    blank: function(a) {return !$.trim("" + a.value);},
    // http://docs.jquery.com/Plugins/Validation/filled
    filled: function(a) {return !!$.trim("" + a.value);},
    // http://docs.jquery.com/Plugins/Validation/unchecked
    unchecked: function(a) {return !a.checked;}
});

// constructor for validator
$.validator = function( options, form ) {
    this.settings = $.extend( true, {}, $.validator.defaults, options );
    this.currentForm = form;
    this.init();
};

$.validator.format = function(source, params) {
    if ( arguments.length == 1 )
        return function() {
            var args = $.makeArray(arguments);
            args.unshift(source);
            return $.validator.format.apply( this, args );
        };
    if ( arguments.length > 2 && params.constructor != Array  ) {
        params = $.makeArray(arguments).slice(1);
    }
    if ( params.constructor != Array ) {
        params = [ params ];
    }
    $.each(params, function(i, n) {
        source = source.replace(new RegExp("\\{" + i + "\\}", "g"), n);
    });
    return source;
};

$.extend($.validator, {

    defaults: {
        messages: {},
        groups: {},
        rules: {},
        errorClass: "error",
        validClass: "valid",
        errorElement: "label",
        focusInvalid: true,
        errorContainer: $( [] ),
        errorLabelContainer: $( [] ),
        onsubmit: true,
        ignore: ":hidden",
        ignoreTitle: false,
        onfocusin: function(element, event) {
            this.lastActive = element;

            // hide error label and remove error class on focus if enabled
            if ( this.settings.focusCleanup && !this.blockFocusCleanup ) {
                this.settings.unhighlight && this.settings.unhighlight.call( this, element, this.settings.errorClass, this.settings.validClass );
                this.addWrapper(this.errorsFor(element)).hide();
            }
        },
        onfocusout: function(element, event) {
            if ( !this.checkable(element) && (element.name in this.submitted || !this.optional(element)) ) {
                this.element(element);
            }
        },
        onkeyup: function(element, event) {
            if ( element.name in this.submitted || element == this.lastElement ) {
                this.element(element);
            }
        },
        onclick: function(element, event) {
            // click on selects, radiobuttons and checkboxes
            if ( element.name in this.submitted )
                this.element(element);
            // or option elements, check parent select in that case
            else if (element.parentNode.name in this.submitted)
                this.element(element.parentNode);
        },
        highlight: function(element, errorClass, validClass) {
            if (element.type === 'radio') {
                this.findByName(element.name).addClass(errorClass).removeClass(validClass);
            } else {
                $(element).addClass(errorClass).removeClass(validClass);
            }
        },
        unhighlight: function(element, errorClass, validClass) {
            if (element.type === 'radio') {
                this.findByName(element.name).removeClass(errorClass).addClass(validClass);
            } else {
                $(element).removeClass(errorClass).addClass(validClass);
            }
        }
    },

    // http://docs.jquery.com/Plugins/Validation/Validator/setDefaults
    setDefaults: function(settings) {
        $.extend( $.validator.defaults, settings );
    },

    messages: {
        required: "This field is required.",
        remote: "Please fix this field.",
        email: "Please enter a valid email address.",
        url: "Please enter a valid URL.",
        date: "Please enter a valid date.",
        dateISO: "Please enter a valid date (ISO).",
        number: "Please enter a valid number.",
        digits: "Please enter only digits.",
        creditcard: "Please enter a valid credit card number.",
        equalTo: "Please enter the same value again.",
        accept: "Please enter a value with a valid extension.",
        maxlength: $.validator.format("Please enter no more than {0} characters."),
        minlength: $.validator.format("Please enter at least {0} characters."),
        rangelength: $.validator.format("Please enter a value between {0} and {1} characters long."),
        range: $.validator.format("Please enter a value between {0} and {1}."),
        max: $.validator.format("Please enter a value less than or equal to {0}."),
        min: $.validator.format("Please enter a value greater than or equal to {0}.")
    },

    autoCreateRanges: false,

    prototype: {

        init: function() {
            this.labelContainer = $(this.settings.errorLabelContainer);
            this.errorContext = this.labelContainer.length && this.labelContainer || $(this.currentForm);
            this.containers = $(this.settings.errorContainer).add( this.settings.errorLabelContainer );
            this.submitted = {};
            this.valueCache = {};
            this.pendingRequest = 0;
            this.pending = {};
            this.invalid = {};
            this.reset();

            var groups = (this.groups = {});
            $.each(this.settings.groups, function(key, value) {
                $.each(value.split(/\s/), function(index, name) {
                    groups[name] = key;
                });
            });
            var rules = this.settings.rules;
            $.each(rules, function(key, value) {
                rules[key] = $.validator.normalizeRule(value);
            });

            function delegate(event) {
                var validator = $.data(this[0].form, "validator"),
                    eventType = "on" + event.type.replace(/^validate/, "");
                validator.settings[eventType] && validator.settings[eventType].call(validator, this[0], event);
            }
            $(this.currentForm)
                   .validateDelegate("[type='text'], [type='password'], [type='file'], select, textarea, " +
                        "[type='number'], [type='search'] ,[type='tel'], [type='url'], " +
                        "[type='email'], [type='datetime'], [type='date'], [type='month'], " +
                        "[type='week'], [type='time'], [type='datetime-local'], " +
                        "[type='range'], [type='color'] ",
                        "focusin focusout keyup", delegate)
                .validateDelegate("[type='radio'], [type='checkbox'], select, option", "click", delegate);

            if (this.settings.invalidHandler)
                $(this.currentForm).bind("invalid-form.validate", this.settings.invalidHandler);
        },

        // http://docs.jquery.com/Plugins/Validation/Validator/form
        form: function() {
            this.checkForm();
            $.extend(this.submitted, this.errorMap);
            this.invalid = $.extend({}, this.errorMap);
            if (!this.valid())
                $(this.currentForm).triggerHandler("invalid-form", [this]);
            this.showErrors();
            return this.valid();
        },

        checkForm: function() {
            this.prepareForm();
            for ( var i = 0, elements = (this.currentElements = this.elements()); elements[i]; i++ ) {
                this.check( elements[i] );
            }
            return this.valid();
        },

        // http://docs.jquery.com/Plugins/Validation/Validator/element
        element: function( element ) {
            element = this.validationTargetFor( this.clean( element ) );
            this.lastElement = element;
            this.prepareElement( element );
            this.currentElements = $(element);
            var result = this.check( element );
            if ( result ) {
                delete this.invalid[element.name];
            } else {
                this.invalid[element.name] = true;
            }
            if ( !this.numberOfInvalids() ) {
                // Hide error containers on last error
                this.toHide = this.toHide.add( this.containers );
            }
            this.showErrors();
            return result;
        },

        // http://docs.jquery.com/Plugins/Validation/Validator/showErrors
        showErrors: function(errors) {
            if(errors) {
                // add items to error list and map
                $.extend( this.errorMap, errors );
                this.errorList = [];
                for ( var name in errors ) {
                    this.errorList.push({
                        message: errors[name],
                        element: this.findByName(name)[0]
                    });
                }
                // remove items from success list
                this.successList = $.grep( this.successList, function(element) {
                    return !(element.name in errors);
                });
            }
            this.settings.showErrors
                ? this.settings.showErrors.call( this, this.errorMap, this.errorList )
                : this.defaultShowErrors();
        },

        // http://docs.jquery.com/Plugins/Validation/Validator/resetForm
        resetForm: function() {
            if ( $.fn.resetForm )
                $( this.currentForm ).resetForm();
            this.submitted = {};
            this.lastElement = null;
            this.prepareForm();
            this.hideErrors();
            this.elements().removeClass( this.settings.errorClass );
        },

        numberOfInvalids: function() {
            return this.objectLength(this.invalid);
        },

        objectLength: function( obj ) {
            var count = 0;
            for ( var i in obj )
                count++;
            return count;
        },

        hideErrors: function() {
            this.addWrapper( this.toHide ).hide();
        },

        valid: function() {
            return this.size() == 0;
        },

        size: function() {
            return this.errorList.length;
        },

        focusInvalid: function() {
            if( this.settings.focusInvalid ) {
                try {
                    $(this.findLastActive() || this.errorList.length && this.errorList[0].element || [])
                    .filter(":visible")
                    .focus()
                    // manually trigger focusin event; without it, focusin handler isn't called, findLastActive won't have anything to find
                    .trigger("focusin");
                } catch(e) {
                    // ignore IE throwing errors when focusing hidden elements
                }
            }
        },

        findLastActive: function() {
            var lastActive = this.lastActive;
            return lastActive && $.grep(this.errorList, function(n) {
                return n.element.name == lastActive.name;
            }).length == 1 && lastActive;
        },

        elements: function() {
            var validator = this,
                rulesCache = {};

            // select all valid inputs inside the form (no submit or reset buttons)
            return $(this.currentForm)
            .find("input, select, textarea")
            .not(":submit, :reset, :image, [disabled]")
            .not( this.settings.ignore )
            .filter(function() {
                !this.name && validator.settings.debug && window.console && console.error( "%o has no name assigned", this);

                // select only the first element for each name, and only those with rules specified
                if ( this.name in rulesCache || !validator.objectLength($(this).rules()) )
                    return false;

                rulesCache[this.name] = true;
                return true;
            });
        },

        clean: function( selector ) {
            return $( selector )[0];
        },

        errors: function() {
            return $( this.settings.errorElement + "." + this.settings.errorClass, this.errorContext );
        },

        reset: function() {
            this.successList = [];
            this.errorList = [];
            this.errorMap = {};
            this.toShow = $([]);
            this.toHide = $([]);
            this.currentElements = $([]);
        },

        prepareForm: function() {
            this.reset();
            this.toHide = this.errors().add( this.containers );
        },

        prepareElement: function( element ) {
            this.reset();
            this.toHide = this.errorsFor(element);
        },

        check: function( element ) {
            element = this.validationTargetFor( this.clean( element ) );

            var rules = $(element).rules();
            var dependencyMismatch = false;
            for (var method in rules ) {
                var rule = { method: method, parameters: rules[method] };
                try {
                    var result = $.validator.methods[method].call( this, element.value.replace(/\r/g, ""), element, rule.parameters );

                    // if a method indicates that the field is optional and therefore valid,
                    // don't mark it as valid when there are no other rules
                    if ( result == "dependency-mismatch" ) {
                        dependencyMismatch = true;
                        continue;
                    }
                    dependencyMismatch = false;

                    if ( result == "pending" ) {
                        this.toHide = this.toHide.not( this.errorsFor(element) );
                        return;
                    }

                    if( !result ) {
                        this.formatAndAdd( element, rule );
                        return false;
                    }
                } catch(e) {
                    this.settings.debug && window.console && console.log("exception occured when checking element " + element.id
                         + ", check the '" + rule.method + "' method", e);
                    throw e;
                }
            }
            if (dependencyMismatch)
                return;
            if ( this.objectLength(rules) )
                this.successList.push(element);
            return true;
        },

        // return the custom message for the given element and validation method
        // specified in the element's "messages" metadata
        customMetaMessage: function(element, method) {
            if (!$.metadata)
                return;

            var meta = this.settings.meta
                ? $(element).metadata()[this.settings.meta]
                : $(element).metadata();

            return meta && meta.messages && meta.messages[method];
        },

        // return the custom message for the given element name and validation method
        customMessage: function( name, method ) {
            var m = this.settings.messages[name];
            return m && (m.constructor == String
                ? m
                : m[method]);
        },

        // return the first defined argument, allowing empty strings
        findDefined: function() {
            for(var i = 0; i < arguments.length; i++) {
                if (arguments[i] !== undefined)
                    return arguments[i];
            }
            return undefined;
        },

        defaultMessage: function( element, method) {
            return this.findDefined(
                this.customMessage( element.name, method ),
                this.customMetaMessage( element, method ),
                // title is never undefined, so handle empty string as undefined
                !this.settings.ignoreTitle && element.title || undefined,
                $.validator.messages[method],
                "<strong>Warning: No message defined for " + element.name + "</strong>"
            );
        },

        formatAndAdd: function( element, rule ) {
            var message = this.defaultMessage( element, rule.method ),
                theregex = /\$?\{(\d+)\}/g;
            if ( typeof message == "function" ) {
                message = message.call(this, rule.parameters, element);
            } else if (theregex.test(message)) {
                message = jQuery.format(message.replace(theregex, '{$1}'), rule.parameters);
            }
            this.errorList.push({
                message: message,
                element: element
            });

            this.errorMap[element.name] = message;
            this.submitted[element.name] = message;
        },

        addWrapper: function(toToggle) {
            if ( this.settings.wrapper )
                toToggle = toToggle.add( toToggle.parent( this.settings.wrapper ) );
            return toToggle;
        },

        defaultShowErrors: function() {
            for ( var i = 0; this.errorList[i]; i++ ) {
                var error = this.errorList[i];
                this.settings.highlight && this.settings.highlight.call( this, error.element, this.settings.errorClass, this.settings.validClass );
                this.showLabel( error.element, error.message );
            }
            if( this.errorList.length ) {
                this.toShow = this.toShow.add( this.containers );
            }
            if (this.settings.success) {
                for ( var i = 0; this.successList[i]; i++ ) {
                    this.showLabel( this.successList[i] );
                }
            }
            if (this.settings.unhighlight) {
                for ( var i = 0, elements = this.validElements(); elements[i]; i++ ) {
                    this.settings.unhighlight.call( this, elements[i], this.settings.errorClass, this.settings.validClass );
                }
            }
            this.toHide = this.toHide.not( this.toShow );
            this.hideErrors();
            this.addWrapper( this.toShow ).show();
        },

        validElements: function() {
            return this.currentElements.not(this.invalidElements());
        },

        invalidElements: function() {
            return $(this.errorList).map(function() {
                return this.element;
            });
        },

        showLabel: function(element, message) {
            var label = this.errorsFor( element );
            if ( label.length ) {
                // refresh error/success class
                label.removeClass( this.settings.validClass ).addClass( this.settings.errorClass );

                // check if we have a generated label, replace the message then
                label.attr("generated") && label.html(message);
            } else {
                // create label
                label = $("<" + this.settings.errorElement + "/>")
                    .attr({"for":  this.idOrName(element), generated: true})
                    .addClass(this.settings.errorClass)
                    .html(message || "");
                if ( this.settings.wrapper ) {
                    // make sure the element is visible, even in IE
                    // actually showing the wrapped element is handled elsewhere
                    label = label.hide().show().wrap("<" + this.settings.wrapper + "/>").parent();
                }
                if ( !this.labelContainer.append(label).length )
                    this.settings.errorPlacement
                        ? this.settings.errorPlacement(label, $(element) )
                        : label.insertAfter(element);
            }
            if ( !message && this.settings.success ) {
                label.text("");
                typeof this.settings.success == "string"
                    ? label.addClass( this.settings.success )
                    : this.settings.success( label );
            }
            this.toShow = this.toShow.add(label);
        },

        errorsFor: function(element) {
            var name = this.idOrName(element);
            return this.errors().filter(function() {
                return $(this).attr('for') == name;
            });
        },

        idOrName: function(element) {
            return this.groups[element.name] || (this.checkable(element) ? element.name : element.id || element.name);
        },

        validationTargetFor: function(element) {
            // if radio/checkbox, validate first element in group instead
            if (this.checkable(element)) {
                element = this.findByName( element.name ).not(this.settings.ignore)[0];
            }
            return element;
        },

        checkable: function( element ) {
            return /radio|checkbox/i.test(element.type);
        },

        findByName: function( name ) {
            // select by name and filter by form for performance over form.find("[name=...]")
            var form = this.currentForm;
            return $(document.getElementsByName(name)).map(function(index, element) {
                return element.form == form && element.name == name && element  || null;
            });
        },

        getLength: function(value, element) {
            switch( element.nodeName.toLowerCase() ) {
            case 'select':
                return $("option:selected", element).length;
            case 'input':
                if( this.checkable( element) )
                    return this.findByName(element.name).filter(':checked').length;
            }
            return value.length;
        },

        depend: function(param, element) {
            return this.dependTypes[typeof param]
                ? this.dependTypes[typeof param](param, element)
                : true;
        },

        dependTypes: {
            "boolean": function(param, element) {
                return param;
            },
            "string": function(param, element) {
                return !!$(param, element.form).length;
            },
            "function": function(param, element) {
                return param(element);
            }
        },

        optional: function(element) {
            return !$.validator.methods.required.call(this, $.trim(element.value), element) && "dependency-mismatch";
        },

        startRequest: function(element) {
            if (!this.pending[element.name]) {
                this.pendingRequest++;
                this.pending[element.name] = true;
            }
        },

        stopRequest: function(element, valid) {
            this.pendingRequest--;
            // sometimes synchronization fails, make sure pendingRequest is never < 0
            if (this.pendingRequest < 0)
                this.pendingRequest = 0;
            delete this.pending[element.name];
            if ( valid && this.pendingRequest == 0 && this.formSubmitted && this.form() ) {
                $(this.currentForm).submit();
                this.formSubmitted = false;
            } else if (!valid && this.pendingRequest == 0 && this.formSubmitted) {
                $(this.currentForm).triggerHandler("invalid-form", [this]);
                this.formSubmitted = false;
            }
        },

        previousValue: function(element) {
            return $.data(element, "previousValue") || $.data(element, "previousValue", {
                old: null,
                valid: true,
                message: this.defaultMessage( element, "remote" )
            });
        }

    },

    classRuleSettings: {
        required: {required: true},
        email: {email: true},
        url: {url: true},
        date: {date: true},
        dateISO: {dateISO: true},
        dateDE: {dateDE: true},
        number: {number: true},
        numberDE: {numberDE: true},
        digits: {digits: true},
        creditcard: {creditcard: true}
    },

    addClassRules: function(className, rules) {
        className.constructor == String ?
            this.classRuleSettings[className] = rules :
            $.extend(this.classRuleSettings, className);
    },

    classRules: function(element) {
        var rules = {};
        var classes = $(element).attr('class');
        classes && $.each(classes.split(' '), function() {
            if (this in $.validator.classRuleSettings) {
                $.extend(rules, $.validator.classRuleSettings[this]);
            }
        });
        return rules;
    },

    attributeRules: function(element) {
        var rules = {};
        var $element = $(element);

        for (var method in $.validator.methods) {
            var value;
            // If .prop exists (jQuery >= 1.6), use it to get true/false for required
            if (method === 'required' && typeof $.fn.prop === 'function') {
                value = $element.prop(method);
            } else {
                value = $element.attr(method);
            }
            if (value) {
                rules[method] = value;
            } else if ($element[0].getAttribute("type") === method) {
                rules[method] = true;
            }
        }

        // maxlength may be returned as -1, 2147483647 (IE) and 524288 (safari) for text inputs
        if (rules.maxlength && /-1|2147483647|524288/.test(rules.maxlength)) {
            delete rules.maxlength;
        }

        return rules;
    },

    metadataRules: function(element) {
        if (!$.metadata) return {};

        var meta = $.data(element.form, 'validator').settings.meta;
        return meta ?
            $(element).metadata()[meta] :
            $(element).metadata();
    },

    staticRules: function(element) {
        var rules = {};
        var validator = $.data(element.form, 'validator');
        if (validator.settings.rules) {
            rules = $.validator.normalizeRule(validator.settings.rules[element.name]) || {};
        }
        return rules;
    },

    normalizeRules: function(rules, element) {
        // handle dependency check
        $.each(rules, function(prop, val) {
            // ignore rule when param is explicitly false, eg. required:false
            if (val === false) {
                delete rules[prop];
                return;
            }
            if (val.param || val.depends) {
                var keepRule = true;
                switch (typeof val.depends) {
                    case "string":
                        keepRule = !!$(val.depends, element.form).length;
                        break;
                    case "function":
                        keepRule = val.depends.call(element, element);
                        break;
                }
                if (keepRule) {
                    rules[prop] = val.param !== undefined ? val.param : true;
                } else {
                    delete rules[prop];
                }
            }
        });

        // evaluate parameters
        $.each(rules, function(rule, parameter) {
            rules[rule] = $.isFunction(parameter) ? parameter(element) : parameter;
        });

        // clean number parameters
        $.each(['minlength', 'maxlength', 'min', 'max'], function() {
            if (rules[this]) {
                rules[this] = Number(rules[this]);
            }
        });
        $.each(['rangelength', 'range'], function() {
            if (rules[this]) {
                rules[this] = [Number(rules[this][0]), Number(rules[this][1])];
            }
        });

        if ($.validator.autoCreateRanges) {
            // auto-create ranges
            if (rules.min && rules.max) {
                rules.range = [rules.min, rules.max];
                delete rules.min;
                delete rules.max;
            }
            if (rules.minlength && rules.maxlength) {
                rules.rangelength = [rules.minlength, rules.maxlength];
                delete rules.minlength;
                delete rules.maxlength;
            }
        }

        // To support custom messages in metadata ignore rule methods titled "messages"
        if (rules.messages) {
            delete rules.messages;
        }

        return rules;
    },

    // Converts a simple string to a {string: true} rule, e.g., "required" to {required:true}
    normalizeRule: function(data) {
        if( typeof data == "string" ) {
            var transformed = {};
            $.each(data.split(/\s/), function() {
                transformed[this] = true;
            });
            data = transformed;
        }
        return data;
    },

    // http://docs.jquery.com/Plugins/Validation/Validator/addMethod
    addMethod: function(name, method, message) {
        $.validator.methods[name] = method;
        $.validator.messages[name] = message != undefined ? message : $.validator.messages[name];
        if (method.length < 3) {
            $.validator.addClassRules(name, $.validator.normalizeRule(name));
        }
    },

    methods: {

        // http://docs.jquery.com/Plugins/Validation/Methods/required
        required: function(value, element, param) {
            // check if dependency is met
            if ( !this.depend(param, element) )
                return "dependency-mismatch";
            switch( element.nodeName.toLowerCase() ) {
            case 'select':
                // could be an array for select-multiple or a string, both are fine this way
                var val = $(element).val();
                return val && val.length > 0;
            case 'input':
                if ( this.checkable(element) )
                    return this.getLength(value, element) > 0;
            default:
                return $.trim(value).length > 0;
            }
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/remote
        remote: function(value, element, param) {
            if ( this.optional(element) )
                return "dependency-mismatch";

            var previous = this.previousValue(element);
            if (!this.settings.messages[element.name] )
                this.settings.messages[element.name] = {};
            previous.originalMessage = this.settings.messages[element.name].remote;
            this.settings.messages[element.name].remote = previous.message;

            param = typeof param == "string" && {url:param} || param;

            if ( this.pending[element.name] ) {
                return "pending";
            }
            if ( previous.old === value ) {
                return previous.valid;
            }

            previous.old = value;
            var validator = this;
            this.startRequest(element);
            var data = {};
            data[element.name] = value;
            $.ajax($.extend(true, {
                url: param,
                mode: "abort",
                port: "validate" + element.name,
                dataType: "json",
                data: data,
                success: function(response) {
                    validator.settings.messages[element.name].remote = previous.originalMessage;
                    var valid = response === true;
                    if ( valid ) {
                        var submitted = validator.formSubmitted;
                        validator.prepareElement(element);
                        validator.formSubmitted = submitted;
                        validator.successList.push(element);
                        validator.showErrors();
                    } else {
                        var errors = {};
                        var message = response || validator.defaultMessage( element, "remote" );
                        errors[element.name] = previous.message = $.isFunction(message) ? message(value) : message;
                        validator.showErrors(errors);
                    }
                    previous.valid = valid;
                    validator.stopRequest(element, valid);
                }
            }, param));
            return "pending";
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/minlength
        minlength: function(value, element, param) {
            return this.optional(element) || this.getLength($.trim(value), element) >= param;
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/maxlength
        maxlength: function(value, element, param) {
            return this.optional(element) || this.getLength($.trim(value), element) <= param;
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/rangelength
        rangelength: function(value, element, param) {
            var length = this.getLength($.trim(value), element);
            return this.optional(element) || ( length >= param[0] && length <= param[1] );
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/min
        min: function( value, element, param ) {
            return this.optional(element) || value >= param;
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/max
        max: function( value, element, param ) {
            return this.optional(element) || value <= param;
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/range
        range: function( value, element, param ) {
            return this.optional(element) || ( value >= param[0] && value <= param[1] );
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/email
        email: function(value, element) {
            // contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
            return this.optional(element) || /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i.test(value);
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/url
        url: function(value, element) {
            // contributed by Scott Gonzalez: http://projects.scottsplayground.com/iri/
            return this.optional(element) || /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(value);
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/date
        date: function(value, element) {
            return this.optional(element) || !/Invalid|NaN/.test(new Date(value));
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/dateISO
        dateISO: function(value, element) {
            return this.optional(element) || /^\d{4}[\/-]\d{1,2}[\/-]\d{1,2}$/.test(value);
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/number
        number: function(value, element) {
            return this.optional(element) || /^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/.test(value);
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/digits
        digits: function(value, element) {
            return this.optional(element) || /^\d+$/.test(value);
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/creditcard
        // based on http://en.wikipedia.org/wiki/Luhn
        creditcard: function(value, element) {
            if ( this.optional(element) )
                return "dependency-mismatch";
            // accept only spaces, digits and dashes
            if (/[^0-9 -]+/.test(value))
                return false;
            var nCheck = 0,
                nDigit = 0,
                bEven = false;

            value = value.replace(/\D/g, "");

            for (var n = value.length - 1; n >= 0; n--) {
                var cDigit = value.charAt(n);
                var nDigit = parseInt(cDigit, 10);
                if (bEven) {
                    if ((nDigit *= 2) > 9)
                        nDigit -= 9;
                }
                nCheck += nDigit;
                bEven = !bEven;
            }

            return (nCheck % 10) == 0;
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/accept
        accept: function(value, element, param) {
            param = typeof param == "string" ? param.replace(/,/g, '|') : "png|jpe?g|gif";
            return this.optional(element) || value.match(new RegExp(".(" + param + ")$", "i"));
        },

        // http://docs.jquery.com/Plugins/Validation/Methods/equalTo
        equalTo: function(value, element, param) {
            // bind to the blur event of the target in order to revalidate whenever the target field is updated
            // TODO find a way to bind the event just once, avoiding the unbind-rebind overhead
            var target = $(param).unbind(".validate-equalTo").bind("blur.validate-equalTo", function() {
                $(element).valid();
            });
            return value == target.val();
        }

    }

});

// deprecated, use $.validator.format instead
$.format = $.validator.format;

})(jQuery);

// ajax mode: abort
// usage: $.ajax({ mode: "abort"[, port: "uniqueport"]});
// if mode:"abort" is used, the previous request on that port (port can be undefined) is aborted via XMLHttpRequest.abort()
;(function($) {
    var pendingRequests = {};
    // Use a prefilter if available (1.5+)
    if ( $.ajaxPrefilter ) {
        $.ajaxPrefilter(function(settings, _, xhr) {
            var port = settings.port;
            if (settings.mode == "abort") {
                if ( pendingRequests[port] ) {
                    pendingRequests[port].abort();
                }
                pendingRequests[port] = xhr;
            }
        });
    } else {
        // Proxy ajax
        var ajax = $.ajax;
        $.ajax = function(settings) {
            var mode = ( "mode" in settings ? settings : $.ajaxSettings ).mode,
                port = ( "port" in settings ? settings : $.ajaxSettings ).port;
            if (mode == "abort") {
                if ( pendingRequests[port] ) {
                    pendingRequests[port].abort();
                }
                return (pendingRequests[port] = ajax.apply(this, arguments));
            }
            return ajax.apply(this, arguments);
        };
    }
})(jQuery);

// provides cross-browser focusin and focusout events
// IE has native support, in other browsers, use event caputuring (neither bubbles)

// provides delegate(type: String, delegate: Selector, handler: Callback) plugin for easier event delegation
// handler is only called when $(event.target).is(delegate), in the scope of the jquery-object for event.target
;(function($) {
    // only implement if not provided by jQuery core (since 1.4)
    // TODO verify if jQuery 1.4's implementation is compatible with older jQuery special-event APIs
    if (!jQuery.event.special.focusin && !jQuery.event.special.focusout && document.addEventListener) {
        $.each({
            focus: 'focusin',
            blur: 'focusout'
        }, function( original, fix ){
            $.event.special[fix] = {
                setup:function() {
                    this.addEventListener( original, handler, true );
                },
                teardown:function() {
                    this.removeEventListener( original, handler, true );
                },
                handler: function(e) {
                    arguments[0] = $.event.fix(e);
                    arguments[0].type = fix;
                    return $.event.handle.apply(this, arguments);
                }
            };
            function handler(e) {
                e = $.event.fix(e);
                e.type = fix;
                return $.event.handle.call(this, e);
            }
        });
    };
    $.extend($.fn, {
        validateDelegate: function(delegate, type, handler) {
            return this.bind(type, function(event) {
                var target = $(event.target);
                if (target.is(delegate)) {
                    return handler.apply(target, arguments);
                }
            });
        }
    });
})(jQuery);

  $.extend($.validator.prototype, {
    showLabel: function(element, message) {
      var label = this.errorsFor( element );

      if (label.length == 0) {
        var railsGenerated = $(element).next('span.help-inline');
        if (railsGenerated.length) {
          railsGenerated.attr('for', this.idOrName(element))
          railsGenerated.attr('generated', 'true');
          label = railsGenerated;
        }
      }

      if (label.length) {
        // refresh error/success class
        label.removeClass(this.settings.validClass).addClass(this.settings.errorClass);
        // check if we have a generated label, replace the message then
        label.attr('generated') && label.html(message);
      } else {
        // create label
        label = $('<' + this.settings.errorElement + '/>')
          .attr({'for':  this.idOrName(element), generated: true})
          .addClass(this.settings.errorClass)
          .addClass('help-inline')
          .html(message || '');
        if (this.settings.wrapper) {
          // make sure the element is visible, even in IE
          // actually showing the wrapped element is handled elsewhere
          label = label.hide().show().wrap('<' + this.settings.wrapper + '/>').parent();
        }
        if (!this.labelContainer.append(label).length)
          this.settings.errorPlacement
            ? this.settings.errorPlacement(label, $(element))
            : label.insertAfter(element);
      }
      if (!message && this.settings.success) {
        label.text('');
        typeof this.settings.success == 'string'
          ? label.addClass(this.settings.success)
          : this.settings.success(label);
      }
      this.toShow = this.toShow.add(label);
    }
  });
  
  /**
  *
  *  MD5 (Message-Digest Algorithm)
  *  http://www.webtoolkit.info/
  *
  **/
   
  var MD5 = function (string) {
   
      function RotateLeft(lValue, iShiftBits) {
          return (lValue<<iShiftBits) | (lValue>>>(32-iShiftBits));
      }
   
      function AddUnsigned(lX,lY) {
          var lX4,lY4,lX8,lY8,lResult;
          lX8 = (lX & 0x80000000);
          lY8 = (lY & 0x80000000);
          lX4 = (lX & 0x40000000);
          lY4 = (lY & 0x40000000);
          lResult = (lX & 0x3FFFFFFF)+(lY & 0x3FFFFFFF);
          if (lX4 & lY4) {
              return (lResult ^ 0x80000000 ^ lX8 ^ lY8);
          }
          if (lX4 | lY4) {
              if (lResult & 0x40000000) {
                  return (lResult ^ 0xC0000000 ^ lX8 ^ lY8);
              } else {
                  return (lResult ^ 0x40000000 ^ lX8 ^ lY8);
              }
          } else {
              return (lResult ^ lX8 ^ lY8);
          }
      }
   
      function F(x,y,z) { return (x & y) | ((~x) & z); }
      function G(x,y,z) { return (x & z) | (y & (~z)); }
      function H(x,y,z) { return (x ^ y ^ z); }
      function I(x,y,z) { return (y ^ (x | (~z))); }
   
      function FF(a,b,c,d,x,s,ac) {
          a = AddUnsigned(a, AddUnsigned(AddUnsigned(F(b, c, d), x), ac));
          return AddUnsigned(RotateLeft(a, s), b);
      };
   
      function GG(a,b,c,d,x,s,ac) {
          a = AddUnsigned(a, AddUnsigned(AddUnsigned(G(b, c, d), x), ac));
          return AddUnsigned(RotateLeft(a, s), b);
      };
   
      function HH(a,b,c,d,x,s,ac) {
          a = AddUnsigned(a, AddUnsigned(AddUnsigned(H(b, c, d), x), ac));
          return AddUnsigned(RotateLeft(a, s), b);
      };
   
      function II(a,b,c,d,x,s,ac) {
          a = AddUnsigned(a, AddUnsigned(AddUnsigned(I(b, c, d), x), ac));
          return AddUnsigned(RotateLeft(a, s), b);
      };
   
      function ConvertToWordArray(string) {
          var lWordCount;
          var lMessageLength = string.length;
          var lNumberOfWords_temp1=lMessageLength + 8;
          var lNumberOfWords_temp2=(lNumberOfWords_temp1-(lNumberOfWords_temp1 % 64))/64;
          var lNumberOfWords = (lNumberOfWords_temp2+1)*16;
          var lWordArray=Array(lNumberOfWords-1);
          var lBytePosition = 0;
          var lByteCount = 0;
          while ( lByteCount < lMessageLength ) {
              lWordCount = (lByteCount-(lByteCount % 4))/4;
              lBytePosition = (lByteCount % 4)*8;
              lWordArray[lWordCount] = (lWordArray[lWordCount] | (string.charCodeAt(lByteCount)<<lBytePosition));
              lByteCount++;
          }
          lWordCount = (lByteCount-(lByteCount % 4))/4;
          lBytePosition = (lByteCount % 4)*8;
          lWordArray[lWordCount] = lWordArray[lWordCount] | (0x80<<lBytePosition);
          lWordArray[lNumberOfWords-2] = lMessageLength<<3;
          lWordArray[lNumberOfWords-1] = lMessageLength>>>29;
          return lWordArray;
      };
   
      function WordToHex(lValue) {
          var WordToHexValue="",WordToHexValue_temp="",lByte,lCount;
          for (lCount = 0;lCount<=3;lCount++) {
              lByte = (lValue>>>(lCount*8)) & 255;
              WordToHexValue_temp = "0" + lByte.toString(16);
              WordToHexValue = WordToHexValue + WordToHexValue_temp.substr(WordToHexValue_temp.length-2,2);
          }
          return WordToHexValue;
      };
   
      function Utf8Encode(string) {
          string = string.replace(/\r\n/g,"\n");
          var utftext = "";
   
          for (var n = 0; n < string.length; n++) {
   
              var c = string.charCodeAt(n);
   
              if (c < 128) {
                  utftext += String.fromCharCode(c);
              }
              else if((c > 127) && (c < 2048)) {
                  utftext += String.fromCharCode((c >> 6) | 192);
                  utftext += String.fromCharCode((c & 63) | 128);
              }
              else {
                  utftext += String.fromCharCode((c >> 12) | 224);
                  utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                  utftext += String.fromCharCode((c & 63) | 128);
              }
   
          }
   
          return utftext;
      };
   
      var x=Array();
      var k,AA,BB,CC,DD,a,b,c,d;
      var S11=7, S12=12, S13=17, S14=22;
      var S21=5, S22=9 , S23=14, S24=20;
      var S31=4, S32=11, S33=16, S34=23;
      var S41=6, S42=10, S43=15, S44=21;
   
      string = Utf8Encode(string);
   
      x = ConvertToWordArray(string);
   
      a = 0x67452301; b = 0xEFCDAB89; c = 0x98BADCFE; d = 0x10325476;
   
      for (k=0;k<x.length;k+=16) {
          AA=a; BB=b; CC=c; DD=d;
          a=FF(a,b,c,d,x[k+0], S11,0xD76AA478);
          d=FF(d,a,b,c,x[k+1], S12,0xE8C7B756);
          c=FF(c,d,a,b,x[k+2], S13,0x242070DB);
          b=FF(b,c,d,a,x[k+3], S14,0xC1BDCEEE);
          a=FF(a,b,c,d,x[k+4], S11,0xF57C0FAF);
          d=FF(d,a,b,c,x[k+5], S12,0x4787C62A);
          c=FF(c,d,a,b,x[k+6], S13,0xA8304613);
          b=FF(b,c,d,a,x[k+7], S14,0xFD469501);
          a=FF(a,b,c,d,x[k+8], S11,0x698098D8);
          d=FF(d,a,b,c,x[k+9], S12,0x8B44F7AF);
          c=FF(c,d,a,b,x[k+10],S13,0xFFFF5BB1);
          b=FF(b,c,d,a,x[k+11],S14,0x895CD7BE);
          a=FF(a,b,c,d,x[k+12],S11,0x6B901122);
          d=FF(d,a,b,c,x[k+13],S12,0xFD987193);
          c=FF(c,d,a,b,x[k+14],S13,0xA679438E);
          b=FF(b,c,d,a,x[k+15],S14,0x49B40821);
          a=GG(a,b,c,d,x[k+1], S21,0xF61E2562);
          d=GG(d,a,b,c,x[k+6], S22,0xC040B340);
          c=GG(c,d,a,b,x[k+11],S23,0x265E5A51);
          b=GG(b,c,d,a,x[k+0], S24,0xE9B6C7AA);
          a=GG(a,b,c,d,x[k+5], S21,0xD62F105D);
          d=GG(d,a,b,c,x[k+10],S22,0x2441453);
          c=GG(c,d,a,b,x[k+15],S23,0xD8A1E681);
          b=GG(b,c,d,a,x[k+4], S24,0xE7D3FBC8);
          a=GG(a,b,c,d,x[k+9], S21,0x21E1CDE6);
          d=GG(d,a,b,c,x[k+14],S22,0xC33707D6);
          c=GG(c,d,a,b,x[k+3], S23,0xF4D50D87);
          b=GG(b,c,d,a,x[k+8], S24,0x455A14ED);
          a=GG(a,b,c,d,x[k+13],S21,0xA9E3E905);
          d=GG(d,a,b,c,x[k+2], S22,0xFCEFA3F8);
          c=GG(c,d,a,b,x[k+7], S23,0x676F02D9);
          b=GG(b,c,d,a,x[k+12],S24,0x8D2A4C8A);
          a=HH(a,b,c,d,x[k+5], S31,0xFFFA3942);
          d=HH(d,a,b,c,x[k+8], S32,0x8771F681);
          c=HH(c,d,a,b,x[k+11],S33,0x6D9D6122);
          b=HH(b,c,d,a,x[k+14],S34,0xFDE5380C);
          a=HH(a,b,c,d,x[k+1], S31,0xA4BEEA44);
          d=HH(d,a,b,c,x[k+4], S32,0x4BDECFA9);
          c=HH(c,d,a,b,x[k+7], S33,0xF6BB4B60);
          b=HH(b,c,d,a,x[k+10],S34,0xBEBFBC70);
          a=HH(a,b,c,d,x[k+13],S31,0x289B7EC6);
          d=HH(d,a,b,c,x[k+0], S32,0xEAA127FA);
          c=HH(c,d,a,b,x[k+3], S33,0xD4EF3085);
          b=HH(b,c,d,a,x[k+6], S34,0x4881D05);
          a=HH(a,b,c,d,x[k+9], S31,0xD9D4D039);
          d=HH(d,a,b,c,x[k+12],S32,0xE6DB99E5);
          c=HH(c,d,a,b,x[k+15],S33,0x1FA27CF8);
          b=HH(b,c,d,a,x[k+2], S34,0xC4AC5665);
          a=II(a,b,c,d,x[k+0], S41,0xF4292244);
          d=II(d,a,b,c,x[k+7], S42,0x432AFF97);
          c=II(c,d,a,b,x[k+14],S43,0xAB9423A7);
          b=II(b,c,d,a,x[k+5], S44,0xFC93A039);
          a=II(a,b,c,d,x[k+12],S41,0x655B59C3);
          d=II(d,a,b,c,x[k+3], S42,0x8F0CCC92);
          c=II(c,d,a,b,x[k+10],S43,0xFFEFF47D);
          b=II(b,c,d,a,x[k+1], S44,0x85845DD1);
          a=II(a,b,c,d,x[k+8], S41,0x6FA87E4F);
          d=II(d,a,b,c,x[k+15],S42,0xFE2CE6E0);
          c=II(c,d,a,b,x[k+6], S43,0xA3014314);
          b=II(b,c,d,a,x[k+13],S44,0x4E0811A1);
          a=II(a,b,c,d,x[k+4], S41,0xF7537E82);
          d=II(d,a,b,c,x[k+11],S42,0xBD3AF235);
          c=II(c,d,a,b,x[k+2], S43,0x2AD7D2BB);
          b=II(b,c,d,a,x[k+9], S44,0xEB86D391);
          a=AddUnsigned(a,AA);
          b=AddUnsigned(b,BB);
          c=AddUnsigned(c,CC);
          d=AddUnsigned(d,DD);
      }
   
      var temp = WordToHex(a)+WordToHex(b)+WordToHex(c)+WordToHex(d);
   
      return temp.toLowerCase();
  }
