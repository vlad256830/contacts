$(document).ready(function () {
    $('#infTable').DataTable({
        "ajax": "mycontacts/",
        "columns": [
            { "data": "id" },
            { "data": "first_name" },
            { "data": "second_name" },
            { "data": "town" },
            { "data": "country" },
            { "data": "telephone" },
            { "data": "email" },
            { "data": "date_of_birth" },
            { "data": "created_at" },

        ],
        "columnDefs": [
            {
                className: "text-center",
                "targets": 0,
                "width": "5%",
                "searchable": false
            },
            {
                className: "text-center",
                "targets": 1,
                "width": "10%",
                "searchable": true
            },
            {
                className: "text-center",
                "targets": 2,
                "width": "10%",
                "searchable": true
            },
            {
                className: "text-center",
                "targets": 3,
                "width": "10%",
                "searchable": true
            },
            {
                className: "text-center",
                "targets": 4,
                "searchable": true
            },
            {
                className: "text-center",
                "targets": 5,
                "searchable": true
            },
            {
                className: "text-center",
                "targets": 6,
                "searchable": true
            },
            {
                className: "text-center",
                "targets": 7,
                "searchable": true
            },
            {
                className: "text-center",
                "targets": 8,
                "searchable": true
            },

            {
                "targets": 9,
                "data": null,
                "defaultContent": "<button class='btn btn-sm btn-danger del'>Delete</button>"
            }
        ],
        "initComplete": function () {
            this.api().columns([3, 4]).every(function () {
                var column = this;
                var select = $('<select class="form-control"><option value=""></option></select>')
                    .appendTo($(column.footer()).empty())
                    .on('change', function () {
                        var val = $(this).val();
                        column.search(this.value).draw();
                    });

                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        },


    });

    var table = $('#infTable').DataTable();


    $('#infTable tbody').on('click', 'button', function () {
        var answer = confirm("Delete record?");
        if (answer) {
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            var data = table.row($(this).parents('tr')).data();
            var id = data['id']
            //console.log(id);
            var url = "/delete/";
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    id: id,
                    csrfmiddlewaretoken: csrftoken,
                },

                success: function (json) {
                    //console.log(json)
                    table.ajax.reload();

                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + " : " + xhr.response.Text);
                    alert(xhr.response.Text);
                }
            });

            return true;
        } else {
            return false;
        };
    });

    var frm = $('#form-modal');
    frm.submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "addcontact/",
            data: frm.serialize(),

            success: function (response) {
                $("#bntclose").click();
                table.ajax.reload();

            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + " : " + xhr.response.Text);
                alert(xhr.response.Text);
            }
        });
        return false;
    });

    //$("#btnSave").click( function() {
    //    alert('BTN Save click');
    // });

    // $("#btnrefresh").click( function()  {
    //     table.ajax.reload();
    //        }
    //     );

    
    // var pgrbar = $('#progress-bar');
    // $('#form-import-csv').submit(function (e) {
    //     e.preventDefault();
    //     var uploadfrm = $('#form-import-csv');

    //     var fdata = new FormData(uploadfrm).get(0);
        

    //     console.log(fdata);

    //     $.ajax({
    //         type: 'POST',
    //         url: 'importcsv/',
    //         data: fdata,            
    //         enctype: 'multipart/form-data',
    //         contentType: false,
    //         success: function (data) {
    //             if (data.task_id != null) {
    //                 get_task_info(data.task_id);
    //             }
    //         },
    //         error: function (data) {
    //             console.log("Something went wrong!");
    //         }
    //     });
    //     return false;
    // });

    // var linfo = $('#labelinfo');
    // function get_task_info(task_id) {
    //     $.ajax({
    //         type: 'get',
    //         url: '/get-task-info/',
    //         data: { 'task_id': task_id },
    //         success: function (data) {
    //             linfo.html('');
    //             if (data.state == 'PENDING') {
    //                 linfo.html('Please wait...');
    //             }
    //             else if (data.state == 'PROGRESS' || data.state == 'SUCCESS') {
    //                 pgrbar.css('display', 'inline');
    //                 pgrbar.val(data.result.percent);
    //                 linfo.html('Contacts created ' + data.result.current + ' out of ' + data.result.total);
    //             }
    //             if (data.state == 'SUCCESS') {
    //                 linfo.html('All contacts created, create ' + data.result.current + ' out of ' + data.result.total);
    //             }
    //             else {
    //                 setTimeout(function () {
    //                     get_task_info(task_id)
    //                 }, 1000);
    //             }

    //         },
    //         error: function (data) {
    //             frm.html("Something went wrong!");
    //         }
    //     });
    // }


});
