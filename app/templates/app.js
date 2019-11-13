function login() {
    $.ajax({
        url: 'http://127.0.0.1:5000/login/',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
                'emailadd': $("#emailadd").val(),
                'pswd': $("#pswd").val()
        }),
        type: "POST",
        dataType: "json",
        success: function (resp) {
            console.log(resp.status);
            if (resp.status == 'ok') {
                window.location.replace('dashboard.html?emailaddress='+resp.message+'/');
            }

            else {
               window.location.replace('login.html?emailaddress='+resp.message+'/');
                //alert.message('Hello!')
            }
        },

        error: function(e){
            alert("danger! Something went wrong in logging in!");
        },

        beforeSend: function (xhrObj){
                xhrObj.setRequestHeader("Authorization",
                "Basic " + btoa("Flask:FlaskDevelopment"));
        }

    });
}