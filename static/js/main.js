$( document ).ready(function() {
    $('#bus_register').submit(function(event) {
        event.preventDefault();
        $('#bus_register_button').prop('disabled', true);
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
            $('#messages').addClass('starter-template');
            $("#messages").html('<p class="bg-danger">' + response.responseText + '</p>');
            $('#bus_register_button').prop('disabled', false);
        });
    });
    $('#ben_register').submit(function(event) {
        event.preventDefault();
        $('#ben_register_button').prop('disabled', true);
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
            $('#messages').addClass('starter-template');
            $("#messages").html('<p class="bg-danger">' + response.responseText + '</p>');
            $('#ben_register_button').prop('disabled', false);
        });
    });
    
    $('#bus_register_option').click(function() {
        $('#bus_register').removeClass('hidden');
        $('#ben_register').addClass('hidden');
    });
    
    $('#ben_register_option').click(function() {
        $('#bus_register').addClass('hidden');
        $('#ben_register').removeClass('hidden');
    });
});