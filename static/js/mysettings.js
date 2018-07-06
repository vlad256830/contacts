$(function(){
    $(".del").click(function(){
        if (!confirm("Do you want to delete")){
          return false;
        }
    });

    frm = $('#form-changepassword');
    frm.submit(function(e) {
        e.preventDefault();
        //console.log('changepassword')
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

    frm = $('#form-vero');
    frm.submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "edit_getvero_key/",            
            data: frm.serialize(),            
            
            success: function(response) { 
                var tkey = $('#id_getvero_key').val();
                var tuser = $('#id_getvero_username').val();
                $('.tkey').html(tkey);
                $('.tuser').html(tuser);

                $("#bntcloseVero").click();            
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + " : " + xhr.response.Text);
                alert(xhr.response.Text);
            }
        });
        return false;
    });
});