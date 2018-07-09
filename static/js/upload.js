$(function () {
  var linfo = $('#labelinfo');
  var pgrbar = $('#progress-bar');
  $(".js-upload-file").click(function () {
 
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (data) {   
        console.log(data.task_id);
        linfo.val(data.task_id);
        if (data.task_id != null) {
          get_task_info(data.task_id);
          linfo.val(data.task_id);
      }
    }
   
  });


  function get_task_info(task_id) {
    console.log(task_id);
        $.ajax({
            type: 'get',
            url: '/get-task-info/',
            data: { 'task_id': task_id },
            success: function (data) {
                linfo.html('');
                if (data.state == 'PENDING') {
                    linfo.html('Please wait...');
                }
                else if (data.state == 'PROGRESS' || data.state == 'SUCCESS') {
                    pgrbar.css('display', 'inline');
                    pgrbar.val(data.result.percent);
                    linfo.html('Contacts created ' + data.result.current + ' out of ' + data.result.total);
                }
                if (data.state == 'SUCCESS') {
                    linfo.html('All contacts created, create ' + data.result.current + ' out of ' + data.result.total);
                }
                else {
                    setTimeout(function () {
                        get_task_info(task_id)
                    }, 1000);
                }

            },
            error: function (data) {
                frm.html("Something went wrong!");
            }
        });
    };

});