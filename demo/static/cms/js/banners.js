$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");

        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        //通过保存按钮上的属性data-type，获取数据类型，如果它的值是update,就是编辑操作了，否则就是添加操作
        var submitType = self.attr('data-type');
        //这里通过保存按钮上的属性data-id获取到轮播图的id, 如果是添加轮播图这就是个空值，不用管它
        var bannerId = self.attr("data-id");

        if(!name || !image_url || !link_url || !priority){
            xtalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }

        //根据submitType的值来判断url应该是添加还是编辑
        var url = '';
        if(submitType == 'update'){
            url = '/cms/ubanner/';
        }else{
            url = '/cms/abanner/';
        }

        bbsajax.post({
            "url": url,   //这里就要改成动态获取上面的url了
            "data": {
                'name':name,
                'image_url': image_url,
                'link_url': link_url,
                'priority':priority,
                'banner_id': bannerId    //这里需要多传入一个轮播图id，就是是添加操作也无所谓，后端也没接收
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                xtalert.alertNetworkError();
            }

        });
    });
});

$(function () {
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type",'update');
        saveBtn.attr('data-id',tr.attr('data-id'));
    });
});

$(function () {
    $(".delete-banner-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        xtalert.alertConfirm({
            "msg":"您确定要删除这个轮播图吗？",
            'confirmCallback': function () {
                bbsajax.post({
                    'url': '/cms/dbanner/',
                    'data':{
                        'banner_id': banner_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            xtalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});

$(function () {
    bbsqiniu.setUp({
        'domain': 'http://pq0cuhzt7.bkt.clouddn.com/',   //七牛的域名
        'browse_btn': 'upload-btn',   //按钮的id
        'uptoken_url': '/c/uptoken/',   //后端的url获取token
        'success': function (up,file,info) {
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);   //把图片的完整地址填入到表单中
        }
    });
});
