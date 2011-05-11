/* Javascript Functions for the index page.
 * Copyright (c) 2011 D. Robert Adams
 */

/* ===========================================================================
 * Called when the main web page is finished loading.
 */
$(document).ready(function()
{
    // Hide the upload document form and attach a click handler to toggle its display.
    $("#upload_form").hide();
    $("#upload_form_label").click(function() {
        $('#upload_form').toggle('blind');
     	return false;
    });
    
    // Fetch the list of documents available to this user and display them
    // as <li><a href="/document/KEY">TITLE</a></li>
    var author = $("#nickname").html();
    $.ajax({
        url: "/rest/document",
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
