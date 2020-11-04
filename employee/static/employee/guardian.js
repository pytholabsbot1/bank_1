if (!$) {
    $ = django.jQuery;
}

$(document).ready(function (){
    $('#id_guardian_name').attr("readonly","readonly");
    $('#id_guardian_address').attr("readonly","readonly");
    $('#id_guardian_relation').attr("disabled","disabled");
    $('#id_minor_checkbox').click(function() {
        if($(this).is(":checked"))
        {
            $('#id_guardian_name').removeAttr("readonly");
            $('#id_guardian_address').removeAttr("readonly");
            $('#id_guardian_relation').removeAttr("disabled");
        }
        else
        {
            $('#id_guardian_name').attr("readonly","readonly").val('');
            $('#id_guardian_address').attr("readonly","readonly").val('');
            $('#id_guardian_relation').attr("disabled","disabled").val('');
        }
    });
});