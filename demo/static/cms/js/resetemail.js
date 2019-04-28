$(function () {
    $('#get_captcha').click(function (event) {
        event.preventDefault();
        var email = $('input[name=email]').val();
        if(!email){
            xtalert.alertInfoToast('请输入邮箱');
            return;
        }

        bbsajax.get({
            'url': '/cms/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] === 200){
                    xtalert.alertSuccessToast(data['message']);
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
        })
    })
});
$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var emailE = $('input[name=email]');
        var captchaE = $('input[name=captcha]');

        var email = emailE.val();
        var captcha = captchaE.val();

        bbsajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] === 200){
                    xtalert.alertSuccessToast(data['message']);
                    emailE.val('');
                    captchaE.val('');
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
        })
    })
});