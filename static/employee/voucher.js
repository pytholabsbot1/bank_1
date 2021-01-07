

$(document).ready(function (){
    if (!$) {
        $ = django.jQuery;
    }
    $('#id_curr_cash').attr("readonly","readonly");
    $('#id_curr_bank').attr("readonly","readonly");
});
