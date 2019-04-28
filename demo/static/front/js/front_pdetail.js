$(function () {
    var ue = UE.getEditor("editor",{
        'serverUrl': '/ueditor/upload/',
        //因为是评论，富文本比编辑器不需要那么多功能，所以这里只列出要用的
        //一个列表代表一行
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    //把ue设置为全局
    window.ue = ue;
});

$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            window.location = '/signin/';
        }else{
            var content = window.ue.getContent();
            var post_id = $("#post-content").attr("data-id");
            bbsajax.post({
                'url': '/acomment/',
                'data':{
                    'content': content,
                    'post_id': post_id
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        window.location.reload();
                    }else{
                        xtalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});