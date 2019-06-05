$(function () {
   $('.sort-select').change(function (event) {
       var value = $(this).val();
       var newHref = bbsparam.setParam(window.location.href,'sort',value);
       window.location = newHref;
   });
});
