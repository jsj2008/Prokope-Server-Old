/* Javascript functions for the page that displays documents and comments.
 * Copyright (c) 2011 D. Robert Adams
 */
 
MAX_COMMENT_LENGTH = 150;

var DocKey  // The unique key for the document being displayed.

/* ===========================================================================
 * Called when the web page is finished loading.
 */
$(document).ready(function()
{
    // Grab the document key for ease of use.
    DocKey = $("#document_id").html();
    
    // Hide the upload forms and attach a click handler to toggle its display.
    $.each(["#upload_comment_form", "#upload_vocab_form", "#upload_sidebar_form"], function(index, form) {   
        $(form).hide();
        $(form+"_label").click(function() {
            // This is called when the user clicks on the label.
            clearForm(form);                                                // clear the form
            $(form).toggle('blind');                                        // display the form
            $(form + " input[name='doc_key']").val(DocKey);    // store the document key
         	return false;
        });
    });
 
});

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


