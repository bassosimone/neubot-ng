/* neubot/www/js/i18n.js */
/*-
 * Copyright (c) 2011 Alessio Palmero Aprosio <alessio@apnetwork.it>,
 *  Universita' degli Studi di Milano
 *
 * This file is part of Neubot <http://www.neubot.org/>.
 *
 * Neubot is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Neubot is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Neubot.  If not, see <http://www.gnu.org/licenses/>.
 */

var LANG = {};

var i18n = {

    get: function(label) {
        if (LANG[label]) {
            return LANG[label];
        }
        else {
            return label;
        }
    },

    getLanguageInUse: function() {
        var lang = undefined;

        jQuery.ajax({
            url: utils.makeURL('/api/config'),
            data: {},
            type: 'GET',
            dataType: 'json',
            error: function() {
                return;
            },
            success: function(data) {
                lang = data['www.lang'];
            }
        });

        if (!lang || lang == 'default') {
            if (navigator.userLanguage) {
                lang = navigator.userLanguage.toLowerCase().substring(0,2);
            }
            else if (navigator.language) {
                lang = navigator.language.toLowerCase().substring(0,2);
            }
        }

        return lang;
    },

    translate_page: function(data, patt) {
        jQuery(".i18n").each(function(index, element) {
            var classList = jQuery(element).attr('class').split(/\s+/);
            jQuery.each(classList, function(i, v) {
                if ((result = patt.exec(v)) && LANG[result[1]]) {
                    switch (element.tagName.toLowerCase()) {
                    case "textarea":
                        jQuery(element).text(LANG[result[1]]);
                        break;
                    default:
                        jQuery(element).html(LANG[result[1]]);
                        break;
                    }
                }
            });
        });
    },

    translate: function() {

        var lang = this.getLanguageInUse();

        jQuery.ajax({
            url: "lang/" + lang + ".js",
            dataType: 'script',
            context: this,
            error: function () {
                jQuery(".i18n").css("visibility", "visible");
            },
            success: function(data) {
                this.translate_page(data, /^(i18n_.*)$/i);
                jQuery(".i18n").css("visibility", "visible");
            }
        });
    }
};

