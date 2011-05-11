/* Javascript Functions for the index page.
 * Copyright (c) 2010 D. Robert Adams
 */

/* ===========================================================================
 * Called when the main web page is finished loading.
 */
$(document).ready(function()
{
    // Fetch the list of documents available to this user and display them
    // as <li><a href="/document/KEY">TITLE</a></li>
    $.ajax({
        url: "/rest/document?include_props=key,title",
        dataType: "xml",
        success: function(xml) {
            $("#doc_list").html(""); // clear out the current list
            $(xml).find('document').each( function() {
                  var li = $("<li/>");  // build a li
                  var a  = $("<a/>").attr( "href", "/document/" + $(this).find('key').text() );
                  $(a).html( $(this).find('title').text() );
                  $(li).append(a);
                  $("#doc_list").append(li);   
            });
        }
    });
});
