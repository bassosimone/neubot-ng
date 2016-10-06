/*-
 * This file is part of Neubot <http://www.neubot.org/>.
 *
 * Neubot is free software. See AUTHORS and LICENSE for more
 * information on the copying conditions.
 */

//
// The "main" of Neubot web interface.
//

// TODO: move this function inside .ready() to
// avoid polluting the function space
function process_state(data) {

    var now = utils.getNow();
    var value = '';

    if (data.events.pid) {
        jQuery("#pid").text(data.events.pid);
    }

    if (data.events.next_rendezvous) {
        value = utils.getTimeFromSeconds(data.events.next_rendezvous);
        // The sysadmin might have adjusted the clock
        if (value && value > now) {
            jQuery("#next_rendezvous").text(utils.formatMinutes(value - now));
        }
    }

    if (data.events.since) {
        value = utils.getTimeFromSeconds(data.events.since, true);
        if (value) {
            jQuery("#since").text(value);
        }
    }

    if (data.events.negotiate) {
        if (data.events.negotiate.queue_pos) {
            jQuery("#queuePos").text(data.events.negotiate.queue_pos);
        }
        else {
            jQuery("#queuePos").text(0);
        }
    }

    if (data.events.test_name) {
        jQuery("#testName").text(data.events.test_name);
    }
}

jQuery(document).ready(function() {
    var section, link;

    // We need this to use jqplot.
    jQuery.jqplot.config.enablePlugins = true;

    //
    // This starts a function that runs periodically to
    // track the state of the Neubot process.
    //
    tracker = state.tracker(function(){});
    tracker.start();

    //
    // By default load the status.html page
    //
    $("#content").load("status.html", function() {
        utils.setActiveTab("status");
        i18n.translate();
    });

    //
    // Arrange things so that when we click on a button we
    // change "tab" in the UX:
    //
    $(".sect").click(function () {
        section = $(this).attr("id");
        section = section.substring(0, section.indexOf("link"));
        link = section + ".html";
        $("#content").load(link, function () {
            utils.setActiveTab(section);
            i18n.translate();
        });
    });
});        
