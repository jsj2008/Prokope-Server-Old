/* Javascript functions for the page that displays documents and comments.
 * Copyright (c) 2010 D. Robert Adams
 */
 
MAX_COMMENT_LENGTH = 150;

var DocKey  // The unique key for the document being displayed.

/* ===========================================================================
 * Called when the web page is finished loading.
 */
$(document).ready(function()
{   
    // Hide the new media dialog.
    $('#media_form').dialog( { autoOpen: false, width: 500 } );
    
    // Hide the upload commentary form and attach a click handler to toggle its display.
    $("#upload_comment_form_label").hide();
    $("#upload_comment_form").hide();
    $("#upload_comment_form_label").click(function() {
        $('#upload_comment_form').toggle('blind');
     	return false;
    });
    
    // Get the id of the document to display from the URL.  The URL should
    // be "show/KEY".  If not, redirect to the home page.
    DocKey = $(location).attr("pathname").split("/")[2];
    if ( ! DocKey ) {
        window.location = "/";
        return;
    }
    
    // Fetch the document and display it.
    $.ajax({
        url: "/rest/document/" + DocKey,
        dataType: "xml",
        success: function(xml) {
            $("#title").html( $(xml).find('title').text() );
            $("#text").html( $(xml).find('content').text() );
            
            // Make the comment box the same height as the text box.
            $('#comments').height( $('.contentbox').height() ); 
            
            // If the owner of the document is the same as the current user...
            if ( $(xml).find('author').text() == $("#nickname").html() ) {
                
                // Make each word in the text clickable.
                $('w').click( showNewMediaDialog );
                
                // Allow the user to upload comments.
                $("#upload_comment_form_label").show();
            }
        }
    });
    
    // Fetch the comments for this document and display them.
    $.ajax({
        url: "/rest/comment?feq_document=" + DocKey,
        dataType: "xml",
        success: processCommentary
    });
    
    // Fetch the media for this document and display them.
    $.ajax({
        url: "/rest/media?feq_document=" + DocKey + "&include_props=key,author,type,title,date,anchor",
        dataType: "xml",
        success: processMedia
    });
    
    // Store the document key in the comment upload form.
    $('#doc_key').val(DocKey);
    
    // Find all the .show_comment links and hide them.  By default,
    // all comment types are shown.
    $('.show_comment_type').each(function() {
       $(this).toggle(); 
    });
    
    // When a user clicks a .show_comment link show the corresponding
    // comments.
    $('.show_comment_type').click(function() {
        $("span:contains('" + $(this).html() + "')").parent().slideDown();
        $(this).toggle();
    });
});

//===========================================================================
// Adds appropriate event handles to new comments.
// xml: XML data of the comment
// li: HTML LI for the comment
function addCommentEventHandlers(xml, li)
{
    // Add styling to the word with the comment.
    var target = $( "#" + $(xml).find('anchor').text().replace(/\./g, '\\.') ).get(0);
    $(target).addClass("commented");
          
    // Highlight the comment when the word is moused-over.
    $(target).mouseover(function(event) {
        $(li).addClass("selected_comment");
    });
    
    // Un-highlight the comment when the word is moused-out.
    $(target).mouseout(function(event) {
        $(li).removeClass("selected_comment");
    });
}

//===========================================================================
// Builds and returns a LI for a comment (xml comment element)
function buildCommentLi(xml)
{
    // Find the word to which this comment refers.
	// Escape all of the periods in the reference id with two double
	// backslashes.  See http://tinyurl.com/yzv9864	
    var target = $( "#" + $(xml).find('anchor').text().replace(/\./g, '\\.') ).get(0);
    
    // Build a list item (li) for this comment.
    var li = $("<li/>");
    li.attr('xref', $(xml).find('anchor').text());
    
    var spanKey = $("<span/>");
    spanKey.addClass("comment_key");
    spanKey.css("display", "none");
    spanKey.html( $(xml).find('key').text() );
    li.append(spanKey);
    
    var spanTitle = $("<span/>");
    spanTitle.addClass('comment_title');
    
    // If this comment doesn't have a title, use the word.
    var title = $(xml).find('title').text();
    if ( $(xml).find('title').text() == "")
        title = $(target).html();
    spanTitle.html(title);
    li.append(spanTitle);
    li.append(": ");
    
    var spanContent = $("<span/>");
    spanContent.addClass('comment_content');
    spanContent.html($(xml).find('content').text());
    li.append(spanContent);
    
    // If the comment is too long, shorten it and add a "more" link
    // that reveals the rest of the comment.
    if ( $(xml).find('content').text().length > MAX_COMMENT_LENGTH )
        $(spanContent).truncate({more: ' More&gt;&gt;', less: ' &lt;&lt;Less', max_length: MAX_COMMENT_LENGTH});                
    
    li.append(" ");
    var spanType = $("<span/>");
    spanType.addClass('comment_type');
    spanType.html('[' + $(xml).find('type').text() + ']');
    li.append(spanType);
    
    // Make all the comment-type element clickable so it toggles
    // their visibility.
    $(spanType).click(function() {
        // Find all comment-type spans that contain the same comment type
        // as the one clicked.  The parent of those spans are the li
        // comments themselves.  Hide them.
        $("span:contains('" + $(this).html() + "')").parent().slideUp();

        // Find the .show_comment link that displays these kinds of comments.
        $("a:contains('" + $(this).html() + "')").toggle();
    });
    
    var spanPublic = $("<span/>");
    spanPublic.addClass('comment_public');
    spanPublic.html($(xml).find('public').text());
    li.append(spanPublic);
    
    return li;
}

//===========================================================================
// Clears a form.
// From http://www.electrictoolbox.com/jquery-clear-form/
function clearForm(ele) 
{
    $(ele).find(':input').each(function() {
        switch(this.type) {
            case 'password':
            case 'select-multiple':
            case 'text':
            case 'hidden':
            case 'textarea':
                $(this).val('');
                break;
            case 'checkbox':
            case 'radio':
                this.checked = false;
                break;
            case 'select':
                $(this).val("0");
                break;
        }
    });
}

//===========================================================================
// Process a single comment (xml comment element).
function processComment(xml)
{    
    var li = buildCommentLi(xml);
    
    // Append the li to the list.
    $("#comments").append(li);
    
    addCommentEventHandlers(xml, li);
}

//===========================================================================
// Processes all comments coming from the server.
function processCommentary(xml)
{
    $(xml).find('comment').each( function() {
        processComment(this);      
    });
}

//===========================================================================
// Process all media for this document (xml media list).
function processMedia(xml)
{     
    $(xml).find('media').each(function() {
        // Find the word to which this media refers.
		// Escape all of the periods in the reference id with two double
		// backslashes.  See http://tinyurl.com/yzv9864	
        var target = $("#" + $(this).find('anchor').text().replace(/\./g, '\\.') ).get(0);

        if ( $(this).find("type").text().indexOf("image") >= 0 ) {
            // Put a thumbnail next to the target word.
            $(target).after(' <a class="thumb_link" title="' + $(this).find("title").text() + '" href="/media/' +  $(this).find("key").text() + '"><img class="thumbnail" src="/media/' + $(this).find("key").text() + '"/></a>');
        }
        else if ( $(this).find("type").text().indexOf("audio") >= 0 ) {
            // Put an audio icon next to the target word.  Embed a reference
            // to the media itself as an xref attribute.
            $(target).after(' <a class="audio_link" xref="/media/' +  $(this).find("key").text() + '"><img class="audio" src="/images/audio.jpeg" /></a>')
        }
    });

    // Put a lightbox on all media.
    $("a.thumb_link").lightbox({ 
        fileLoadingImage : '/images/loading.gif',
	    fileBottomNavCloseImage : '/images/closelabel.gif'
	});

    // Create the audio player.
    $("#audio_player").jPlayer( { swfPath: "/js" } );

    // Attach a click handler to all audio links.
    $("a.audio_link").click(function() {

        // If we're playing something already, stop it, otherwise, play
        // the selected file.
        if ( $("#audio_player").jPlayer( "getData", "diag.isPlaying" ) ) {
            $("#audio_player").jPlayer("pause");
        }
        else
            // There must be an xref attribute on the audio_link itself that
            // indicates which media to play.
            $("#audio_player").jPlayer( "setFile", $(this).attr("xref") ).jPlayer("play");
    });

}

//===========================================================================
// Displays the new media dialog.
// this refers to the word that was clicked
function showNewMediaDialog(event)
{
    clearForm( $('#media_form') );
    
    // Store the document key in the form.
    $("#media_document").attr( "value", DocKey );
    
    // Put the id of the word being referenced into the form.
    $("#media_anchor").attr( "value", $(this).attr("id") );
    
    // Open the form.
    $('#media_form').dialog("option", "title", 'New Media');
    $('#media_form').dialog('open');
}



