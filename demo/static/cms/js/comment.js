$(function () {
   $('.delete-comment-btn').click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var comment_id = tr.attr('data-id');

       bbsajax.post({
           'url': '/cms/dcomment/',
           'data': {
               'comment_id': comment_id
           },
           'success': function (data) {
               if (data['code'] == 200) {
                   window.location.reload();
               } else {
                   xtalert.alertInfo(data['message'])
               }
           }
       });
   });
});