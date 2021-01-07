
$(document).ready(function (){
    if (!$) {
        $ = django.jQuery;
    }
    $(window).bind("load", function () {
    console.log($(".datetimeshortcuts").remove());
  });
    $('.vForeignKeyRawIdAdminField').attr("readonly","readonly");
    $.get("/bank/deposit_check/", function (data) {
        var data = JSON.parse(data);
        if (!data.admin){
            $("#id_status option:not(:selected)").attr("disabled", "disabled");
        }
    });
});