function message_error(obj){
    var html_tags = '';
    if (typeof (obj) === 'object' ) {
        html_tags = '<ul style="text-align: left;">';
        $.each(obj, function(key, value) {
            html_tags += '<li>' + key + ': ' + value + '</li>';
        });
        html_tags += '</ul>';
    }
    else {
        html_tags = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html_tags,
        icon: 'error'
    });
}