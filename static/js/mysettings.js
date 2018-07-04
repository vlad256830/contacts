$(function(){
    frm = $('#form-changepassword');
    frm.submit(function(e) {
        e.preventDefault();
        console.log('changepassword')
        $.ajax({
            type: "POST",
            url: "changepassword/",            
            data: frm.serialize(),             
            
            success: function(response) {              
                $("#bntclose").click();            
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + " : " + xhr.response.Text);
                alert(xhr.response.Text);
            }
        });
        return false;
    });
});