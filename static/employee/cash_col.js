
function load_(){

    notes = [];
    coins = [];
    $("fieldset")[2].querySelectorAll("input").forEach((el) => {notes.push(el.name.slice(2,) * el.value)});
    $("fieldset")[3].querySelectorAll("input").forEach((el) => {coins.push(el.name.slice(2,) * el.value)});
    
    var notes_num = notes.reduce((a, b) => a + b, 0);
    var coins_num = coins.reduce((a, b) => a + b, 0);
    
    var payments = 0;
    for( var i=0;i<$("h3").length-1 ; i++){ 
        el = $(`[name='emp_payments_set-${i}-amount']`);
        payments = payments + Number(el[0].value);
    }
    
    
    var tot_dp = Number($(`[name='total_society_deposit']`)[0].value) + Number($(`[name='total_loan_deposit']`)[0].value);
    
    console.log(tot_dp , notes_num , payments);

    $("#tot_d")[0].textContent =  "Total Deposit : " + tot_dp;
    $("#tot_p")[0].textContent = "Total Payments : " + payments;
    $("#tot_n")[0].textContent = "Total Notes Amount : " + (notes_num + coins_num);
    $("#check_res")[0].textContent = "Net Amount : " + (tot_dp - payments);
}

function load_past_form(date){
    $.get( "/bank/pastcollection/" + date, function( data ) {
        var data = JSON.parse(data);
        $("#id_total_society_deposit").val(data.d);
        $("#id_total_loan_deposit").val(data.f);
        $("#id_total_cash_collection").val(data.d + data.f);
    });
}

function check_collection() {
    $.get( "/bank/check_collection/", function( data ) {
        var data = JSON.parse(data);
        if (data.collection) {
            alert("Entry for today has already been done! Please Exit.");
            $("#id_total_society_deposit").val(0);
            $("#id_total_loan_deposit").val(0);
        }
      });
}

function emp_payments() {
    var emp_payments = $(".dynamic-emp_payments_set input.vIntegerField");
    var sum = 0;
    for(var i = 0; i < emp_payments.length; i++){
        sum = sum + parseInt($(emp_payments[i]).val());
    }
    console.log(sum);
    var total = parseInt($("#id_total_loan_deposit").val()) + parseInt($("#id_total_society_deposit").val());
    $("#id_total_cash_collection").val(total - sum);
}

window.onload = function(){
    $('#id_total_society_deposit').attr("readonly","readonly");
    $('#id_total_loan_deposit').attr("readonly","readonly");
    $('#id_total_cash_collection').attr("readonly","readonly");
    $('#id_date').attr("readonly","readonly");
    $("#content").prepend(`<div> 
    <button onclick="load_()">Check Details</button>
    <p id="tot_d"></p>
    <p id="tot_p"></p>
    <p id="tot_n"></p>
    <h2 id="check_res"></h2>
    </div>`);
    check_collection();
    var hashParams = window.location.hash.substr(1); // substr(1) to remove the `#`
	hashParams = atob(hashParams);
	hashParams = hashParams.split('&');
    if (hashParams[0]){
        for(var i = 0; i < hashParams.length; i++){
            var p = hashParams[i].split('=');
            document.getElementById(p[0]).value = decodeURIComponent(p[1]);
            load_past_form(p[1]);
            break;
        }
    }
    console.log($( ".dynamic-emp_payments_set input.vIntegerField" ));
    $(document).on('change', '.dynamic-emp_payments_set input.vIntegerField', function() { emp_payments(); });
    var sum = $("#id_total_society_deposit").val() + $("#id_total_loan_deposit").val();
    var checkExist = setInterval(function() {
        if ($('.datetimeshortcuts').length) {
           $(".datetimeshortcuts").remove();
           clearInterval(checkExist);
        }
     }, 100); // check every 100ms
};