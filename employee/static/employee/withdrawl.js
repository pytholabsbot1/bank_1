if (!$) {
    $ = django.jQuery;
}

$(document).ready(function (){
    $("#id_paymode").change(function(){
        if (this.value == 'CASH'){
            $("#id_cheque_no").attr('disabled', 'disabled');
            $('h2:contains("Cash")').parent().show();
            $('h2:contains("Coins")').parent().show();
        }
        else {
            $("#id_cheque_no").removeAttr('disabled');
            $('h2:contains("Cash")').parent().hide();
            $('h2:contains("Coins")').parent().hide();
        }
    });
});