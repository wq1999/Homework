$(function(){
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = bbsparam.setParam(src,'xx',Math.random());
        self.attr('src',newsrc);
    });
});

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var graph_captcha_input = $("input[name='graph_captcha']")

        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        bbsajax.post({
            'url': '/signup/',
            'data': {
                'username': username,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function(data){
                if(data['code'] == 200){
                    var return_to = $("#return-to-span").text();
                    if(return_to){
                        window.location = return_to;
                    }else{
                        window.location = '/';
                    }
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function(){
                xtalert.alertNetworkError();
            }
        });
    });
});
