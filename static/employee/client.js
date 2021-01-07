if (!$) {
    $ = django.jQuery;
}
$(document).ready(function (){
    $('#id_mobile_number_1').prop("type","number");
    $('#id_mobile_number_2').prop("type","number");
    $('#id_landline_number').prop("type","number");
    $('#id_referal_mobile_number').prop("type","number");
    $('#id_contact').prop("type","number");
});