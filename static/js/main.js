$( document ).ready(function() {
    $('#register').submit(function(event) {
        event.preventDefault();
        $('#register_button').prop('disabled', true);
        //get form action url
        var post_url = $(this).attr("action");
        //get form GET/POST method
        var request_method = $(this).attr("method");
        //Encode form elements for submission
        var form_data = $(this).serialize();
        //
        var originURL = location.origin;

        $.ajax({
            url : post_url,
            type: request_method,
            data : form_data
        }).done(function(response) {
            window.location.replace(originURL.concat("/login"));
        }).fail(function(response) {
            $("#messages").html('<p>response</p>');
        });
    });
});