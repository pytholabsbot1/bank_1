if (!$) {
    $ = django.jQuery;
}
$(document).ready(function (){
    $(window).bind("load", function () {
        $(".dynamic-documents_set .datetimeshortcuts").remove();
        $(".add-row a").click(function(){
            $(".dynamic-documents_set .datetimeshortcuts").remove();
        });
      });
    $('.vForeignKeyRawIdAdminField').attr("readonly","readonly");
    $('.field-created_time input').attr("readonly","readonly");
    var lan = $('.field-loan_account_number .readonly').text();
    $.get("/bank/doc_check/" + lan , function (data) {
        var data = JSON.parse(data);
        console.log(data)
        console.log(!data.change)
        console.log(typeof(data.change))
        if (!data.change){
            $(".field-status select option:not(:selected)").attr("disabled","disabled");
            $(".dynamic-documents_set select option:not(:selected)").attr("disabled","disabled");
        }
    });
});