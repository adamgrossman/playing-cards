    $('.more_info').on('click', function () {
        var course = $(this).data('course');
        var id = $(this).attr('id');
        $.ajax({
            url: "/course/"+course,
            type: "GET",
//            dataType: "json",
            success: function (data) {
                $('#courseInfo'+id).html(data);
            },
            error: function (data) {
                console.log('bad');
                console.log(data);
            }
        });
    });