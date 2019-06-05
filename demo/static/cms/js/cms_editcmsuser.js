$(function () {
   $('#submit').click(function (event) {
       event.preventDefault();

       var checkedInputs = $(':checkbox:checked');

       var roles = [];
       checkedInputs.each(function () {
          var role_id = $(this).val();
           roles.push(role_id);
       });
        var user_id = $(this).attr('data-user-id');
        bbsajax.post({
            'url': '/cms/edit_cmsuser/',
            'data':{
                'user_id': user_id,
                'roles': roles
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('恭喜！CMS用户信息修改成功！');
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
   });
});