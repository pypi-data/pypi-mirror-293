/**
 * client side utilities for SJTXE. Required Ext and Underscore libraries.
 * @param root
 * @param Ext
 * @param underscore
 * @returns
 *
 */

function strip_tags(str_val) {
    return str_val.replace(/(<([^>]+)>)/ig,"");
}

(function(root, Ext) {
    var root = root || window;
    var me = root;
    var Ext = Ext;
    /*private vars*/
    var hasAjaxFailure = false;
    var hasAjaxComplete = false;

    var onAjaxError = function(conn, response, options, eOpts) {
        hasAjaxFailure = true;
    };

    root.GeneralEvalElement = {};
    var onAjaxComplete = function(conn, response, options, eOpts) {
        var linit;
        hasAjaxComplete = true;
        if (response.responseText.indexOf('{') != 0 && !response.responseText.includes('<!DOCTYPE html>')) {
            var syntax;
            try {
                syntax = esprima.parse(response.responseText);
            } catch(err) {
                console.log('Esprima parse error!');
                console.log(err.message);
            }

            if (syntax.body[0].expression.callee) {
                if (syntax.body[0].expression.callee.body) {
                    linit = syntax.body[0].expression.callee.body.body[0].declarations[0].init;

                    while (linit.callee && !(linit.callee.property && (linit.callee.property.name === 'Window'
                    || linit.callee.property.name == 'EditWindow'))) {
                        linit = linit.callee.body.body[0].declarations[0].init;
                    }

                    var properties = linit.arguments ? linit.arguments[0].properties : [];
                    var title = '',
                        win_id = '';
                    for (var i = 0; i < properties.length; ++i) {
                        if (properties[i].key.name == 'title')
                            title = strip_tags(properties[i].value.value);
                        if (properties[i].key.name == 'id')
                            win_id = properties[i].value.value;
                    }
                    window.GeneralEvalElement[title] = {
                        'id': win_id
                    };
                };
            }
        }
        /*
            Если в AJAX ответе приходит сообщение
             с именеи файла то сохраняем его
         */
        if (response.responseText.indexOf('media/downloads') != -1) {
            file_name = response.responseText.slice(
                response.responseText.indexOf("/media"),
                response.responseText.indexOf("xls")+3
            );
            window.reportFileName = file_name.split('/').pop();
        }

        if (response.responseText.indexOf('Файл успешно импортирован') != -1) {
            window.responseImport = true;
        }
    };

    Ext.onReady(function() {
        Ext.Ajax.on({
            requestexception: onAjaxError,
            requestcomplete: onAjaxComplete
        });
    });

    //exposed object
    var SJTXE = {
        VERSION: '0.0',
        hasAjaxFailure: function() {
            return hasAjaxFailure
        },
        hasAjaxComplete: function() {
            return hasAjaxComplete
        }
    };
    root.SJTXE = SJTXE;

    return SJTXE;
})(this, Ext);

var assert = function(condition, message) {
    'use strict';
    if (!condition)
        throw Error("Assert failed" + (typeof message !== "undefined" ? ": " + message : ""));
};

window.__webdriver_javascript_errors = [];
window.onerror = function(errorMsg, url, lineNumber) {
    console.log(errorMsg);
    window.__webdriver_javascript_errors.push(
        errorMsg + ' (found at ' + url + ', line ' + lineNumber + ')');
};
