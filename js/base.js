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
});