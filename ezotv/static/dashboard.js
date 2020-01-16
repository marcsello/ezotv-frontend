$(document).ready(function() {

    // Switch between displaying and editing info

    var start_edit_btn = $('#start_edit');

    var cancel_edit_btn = $('#cancel_edit');

    var visibility_items = [ $('#password_verify_group'), $('#submit_group'), $('#submit_group'), $('#minecraft_nameHelpBlock'), $('#passwordHelpBlock') ];
    var input_items = [ $('#minecraft_name') , $('#password'),  $('#password_verify') ];

    start_edit_btn.click(function() {

        start_edit_btn.addClass('d-none');
        cancel_edit_btn.removeClass('d-none');

        $.each(visibility_items, function( index, item ) {
            item.removeClass('d-none');
        });

        $.each(input_items, function( index, item ) {
            item.removeClass('form-control-plaintext');
            item.addClass('form-control');
            item.attr('readonly', false);
        });

    });

    cancel_edit_btn.click(function() {

        cancel_edit_btn.addClass('d-none');
        start_edit_btn.removeClass('d-none');

        $.each(visibility_items, function( index, item ) {
            item.addClass('d-none');
        });

        $.each(input_items, function( index, item ) {
            item.removeClass('form-control');
            item.addClass('form-control-plaintext');
            item.attr('readonly', true);
            item.val(item.data('original'));
        });
        
        $('#minecraft_name').removeClass('bg-warning'); // ugly hax

    });

});


$(document).ready(function() {

    // Password match constraint for the password input field

    var password = $('#password');
    var password_verify = $('#password_verify');
    var minecraft_name = $('#minecraft_name');

    function password_match_check() {
    
        if (password_verify.val() != password.val()) {
            password_verify[0].setCustomValidity('Password Must be Matching.'); // [0] to pull native js element from jQuery
        } else {
            password_verify[0].setCustomValidity(''); // clear the error allowing submit
        }
        
    }
    
    password.change(password_match_check);
    password_verify.change(password_match_check);


    // Highlight on name change
    
    function highlight_on_difference() {
    
        if (minecraft_name.data('original') == '') { // ignore if name not yet set
            return
        }
    
        if (minecraft_name.val() != minecraft_name.data('original')) {
            minecraft_name.addClass('bg-warning');
        } else {
            minecraft_name.removeClass('bg-warning');
        }
    
    
    }

    minecraft_name.on('input',highlight_on_difference);


    // Confirmation on name change
    
    $('#minecraft-data-form').submit(function() {
    
        if (minecraft_name.data('original') == '') { // ignore if name not yet set
            return true;
        }
    
        if (minecraft_name.val() != minecraft_name.data('original')) {
            return confirm("A Minecraft játékos neved megváltoztatására készülsz!\nEz esetben addig nem fogsz tudni játszani, amíg egy adminisztrátor el nem fogadja az új neved!\nBiztosan ezt szeretnéd?");
        } else {
            return true;
        }
    
    });


});