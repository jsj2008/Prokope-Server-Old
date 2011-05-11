/* Javascript functions for the every page that extends base.html.
 * Copyright (c) 2010 D. Robert Adams
 */

$(document).ready(function()
{
    // Prepare the about dialog box.
    $('#about').dialog( {autoOpen: false, title: "About Project Prokope" } );
    $('#about_link').click(function() {
        $('#about').dialog('open');
        return false;
    });
    
    // Prepare the help dialog box.
    $('#help').dialog( {autoOpen: false, title: "Help"} );
    $('#help_link').click(function() {
        $('#help').dialog('open');
        return false;
    });
    
    // Hide the upload document form and attach a click handler to toggle its display.
    $("#upload_form").hide();
    $("#upload_form_label").click(function() {
        $('#upload_form').toggle('blind');
     	return false;
    });
});