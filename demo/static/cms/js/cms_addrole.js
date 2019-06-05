
$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        // 获取组名
        var name = $("input[name='name']").val();
        var desc = $("input[name='desc']").val();
        var role_id = $(this).attr('data-role-id');
        var permission_inputs = $("input[name='permission']:checked");
        var permissions = [];
        $.each(permission_inputs,function (idx,obj) {
            permissions.push($(obj).val());
        });

        var url = null;
        var data = {
            name:name,
            desc:desc,
            permissions: permissions
        };
        if(role_id){
            url = '/cms/edit_role/';
            data['role_id'] = role_id
        }else{
            url = '/cms/add_role/';
        }
        bbsajax.post({
            url: url,
            data: data,
            success: function (data) {
                xtalert.alertSuccessToast('恭喜，CMS组添加成功！');
                setTimeout(function () {
                    // 跳转到组管理页面
                    window.location = '/cms/croles/';
                },1200);
            },
            fail: function (error) {
                console.log(error);
            }
        });
    });
});