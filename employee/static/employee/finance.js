a = 2;
var sc , dt;

function load_past_form(){
	populate();
    // $.get( "/bank/approveloan/" + num, function( data ) {
    //     var data = JSON.parse(data);
    //     console.log(data);
    // });
}

window.onload = function() {
	console.log( "ready!" );
	$("#content").prepend('<div class="loandata"></div>')
	console.log($("#content").prepend('<button onClick=populate()>Load Details</button>'));
	$('#id_finance').attr("readonly","readonly");
	$('#id_person').attr("readonly","readonly");
	$.get("/bank/deposit_check/", function (data) {
        var data = JSON.parse(data);
        if (!data.admin){
			$("#id_status option:not(:selected)").attr("disabled", "disabled");
        }
	});
	var hashParams = window.location.hash.substr(1); // substr(1) to remove the `#`
	hashParams = atob(hashParams);
	hashParams = hashParams.split('&');
	// console.log(typeof(hashParams))
    if (hashParams[0]){
		for(var i = 0; i < hashParams.length; i++){
			var p = hashParams[i].split('=');
            document.getElementById(p[0]).value = decodeURIComponent(p[1]);
            load_past_form(p[1]);
            break;
        }
    }
};

function populate(){
	var code = $("#id_finance").val();
	$.get( "/bank/fc/" + code , function( data ) {
		var data = JSON.parse(data);
		console.log(data);
		// s = '{},'.format(data.id , data.person.nomination_number , data.person.first_name+ ' ' + data.person.last_name , data.demanded_amount , data.expected_date , str(data.loan_duration) + data.duration_type)
	
		var info = `<div style="color: black;"  class="animate__animated animate__bounceInLeft"> 
		<br><br> <p id="client">Nomination no: ${data.nom_num}</p> <p>
		Name : ${data.name}</p> <p> 
		Demanded Amount: ${data.amount}</p> <p>
		Expected Date: ${data.date}</p> <p>
		Duration: ${data.loan_duration} ${data.duration_type}</p></div>`;

		$(".loandata").append(info);
		$("#id_sanctioned_amount").val(data.amount).addClass("animate__animated animate__wobble");
		$("#id_loan_duration").val(data.loan_duration).addClass("animate__animated animate__wobble");
		$('[name=duration_type] option').filter(function() { 
			return ($(this).text() == data.duration_type);
		}).prop('selected', true).addClass("animate__animated animate__wobble");
		$('[name=emi_type] option').filter(function() { 
			return ($(this).text() == data.emi_type);
		}).prop('selected', true);
		$('[name=duration_type]').addClass("animate__animated animate__wobble");
		$('[name=emi_type]').addClass("animate__animated animate__wobble");
		// $("#Code").text('Deposit ID : '+code);
		// $("#client").text('Client Name : '+data[2]);
		// $('input[name ="previous_balance"]').val(data[1]);
		// $('input[name ="latest_intrest"]').val(data[3]);
	  });
}