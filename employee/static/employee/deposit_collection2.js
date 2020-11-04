window.onload = function() {
	$(".datetimeshortcuts").hide()
	console.log( "ready!12" );
	link = window.location.href;
	h = link.includes("deposit");
	if (h){
		
		$("#content").prepend(`<div style="margin-top: 20px;margin-bottom: 20px;"> 
		<button onclick="deposit()">Load Details</button></div>`);
	}
	else if (link.includes("finance")){
		$("#content").prepend(`<div style="margin-top: 20px;margin-bottom: 20px;"> 
		<button onclick="finance()">Load Details</button></div>`);
	}
	if(window.location.href.includes('/add/')){
		var el = '<br><br><label for="qr" style="background-image: linear-gradient(to right, #00d2ff, #3a7bd5 100%, #00d2ff);padding: 10px;color: white;border-radius: 10px;" > Scan QR Code </label><input id="qr" type=file accept="image/*" capture=environment onclick="return showQRIntro();" onchange="openQRCamera(this);" tabindex=-1> <br><br><p id="Code"></p> <br> <p id="client"></p>'
		$($("h1")[1]).append(el);
	}
	href = window.location.href.split("=");
	console.log(href);
	if(href.length==2){
		if(href[1].slice(0,2)=="26"){
			populate(href[1],$('input[name ="loan_emi_received_date"]').val(), "loan");
		}else{
			populate(href[1], $('.field-payment_received_date .readonly').text() , "dp");
		}
	}

	$('#id_previous_balance').attr("readonly","readonly");
	$('#id_latest_intrest').attr("readonly","readonly");
	$('#id_deposit').attr("readonly","readonly");
	$("#id_created_time").attr('readonly', 'readonly');
	$("#id_finance").attr('readonly', 'readonly');
	$("#id_bill_no").attr('readonly', 'readonly');
	$(".field-loan_emi_received_date input").attr('readonly', 'readonly');
};

function populate(code ,dt ,type_){
	var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

dt = `${mm}-${dd}-${yyyy}`;
	if(type_=="dp"){
		$.get( `/bank/coll/${code}`, function( data ) {	
			// format : id , balance , name ,interest
			data = data.split(",");

			if (data[4] == "DEACTIVE") {
				alert("THIS ACCOUNT IS DEACTIVATED. Please contact admin!");
				var delay = 1000; 
				setTimeout(function(){ window.location = '/bank/'; }, delay);
				console.log("REDI");
			}
			
			console.log(data);
			$('input[name ="deposit"]').val(data[0]);
			
			$("#Code").text('Deposit ID : '+code);
			$("#client").text('Client Name : '+data[2]);
			$('input[name ="previous_balance"]').val(data[1]);
			$('input[name ="latest_intrest"]').val(data[3]);
		});
		
	}else{
		$.get( `/bank/fc_coll/${code}` , function( data ) {	
			// format : id , balance , name ,interest
			data = data.split(",");
	
			console.log(data);
			$('input[name ="deposit"]').val(data[0]);
	
			$("#Code").text('Finance ID : '+code);
			$("#client").text('Client Name : '+data[4]);
			$('input[name ="finance"]').val(data[0]);
			$('input[name ="loan_emi_received"]').val(data[1]);
			
			alert(`Client: ${data[4]}\nTotal Recieved: ${data[2]}\nRemaing Amount: ${data[3]}`);
			
		});
	}
	
}


function openQRCamera(node) {
	var reader = new FileReader();
	reader.onload = function() {
		node.value = "";
		qrcode.callback = function(res) {
			if(res instanceof Error) {
				alert("No QR code found. Please make sure the QR code is within the camera's frame and try again.");
			} else {
				console.log(res);
				if (res.startsWith("1")){
					populate(res ,$('.field-payment_received_date .readonly').text(), "dp" );
				}
				else{
					console.log("NOT FIN")
					populate(res ,$('input[name ="payment_received_date"]').val() );
				}
			}
		};
		qrcode.decode(reader.result);
	};
	reader.readAsDataURL(node.files[0]);
}

	
function parse_page(res){
	tp_code = res.slice(0,2);
	if(tp_code=="26"){
		window.location = '/admin/employee/collection_finance/add?q='+res;
	}else{
		window.location = '/admin/employee/collection_deposit/add?q='+res;
	}
}

function openQR(node) {
	var reader = new FileReader();
	reader.onload = function() {
		node.value = "";
		qrcode.callback = function(res) {
		if(res instanceof Error) {
			alert("No QR code found. Please make sure the QR code is within the camera's frame and try again.");
		} else {
			console.log(res);
			parse_page(res);
		}
		};
		qrcode.decode(reader.result);
	};
	reader.readAsDataURL(node.files[0]);
}

function deposit(){
    $.get( "/bank/dep_collection/" + $("#id_deposit").val() , function( data ) {
	   var data = JSON.parse(data);
	   if (data.status == "DEACTIVE") {
		alert("THIS ACCOUNT IS DEACTIVATED. Please contact admin!");
		var delay = 100; 
		setTimeout(function(){ window.location = '/bank/'; }, delay);
		console.log("REDI");
	}
	   $("#id_previous_balance").val(data.balance);
	   $("#id_latest_intrest").val(data.interest);
    });
}

function finance(){
    $.get( "/bank/fin_collection/" + $("#id_finance").val() , function( data ) {
	   var data = JSON.parse(data);
	   if (data.status == "DEACTIVE") {
		alert("THIS ACCOUNT IS DEACTIVATED. Please contact admin!");
		var delay = 500; 
		setTimeout(function(){ window.location = '/bank/'; }, delay);
		console.log("REDI");
	}
	   $("#id_loan_emi_received").val(data.emi);
    });
}


