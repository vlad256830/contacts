$(function () {

  $(".js-upload-file").click(function () {
 
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      if (data.result.is_valid) {
        console.log('data upload')
        
      }
    }
  });

});
