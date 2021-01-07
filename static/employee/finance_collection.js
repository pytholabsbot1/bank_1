

window.onload = function() {
    console.log( "ready!12" );

    if(window.location.href.includes('/add/')){
        var el = '<br><br><label for="qr" style="background-image: linear-gradient(to right, #00d2ff, #3a7bd5 100%, #00d2ff);padding: 10px;color: white;border-radius: 10px;" > Scan QR Code </label><input id="qr" type=file accept="image/*" capture=environment onclick="return showQRIntro();" onchange="openQRCamera(this);" tabindex=-1> <br><br><p id="Code"></p> <br> <p id="client"></p>'
        $($("h1")[1]).append(el);

		var agent_ = window.location.href.split("#")[1];
		$('input[name ="agent_name"]').val(agent_);
		
	}
	
    
};


function populate(code){
	$.get( "/bank/fc_coll/" + code , function( data ) {
		
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

function openQRCamera(node) {
	var reader = new FileReader();
	reader.onload = function() {
		node.value = "";
		qrcode.callback = function(res) {
		if(res instanceof Error) {
			alert("No QR code found. Please make sure the QR code is within the camera's frame and try again.");
		} else {
            console.log(res);
            populate(res);
		}
		};
		qrcode.decode(reader.result);
	};
	reader.readAsDataURL(node.files[0]);
	}

	function showQRIntro() {
	return confirm("Use your camera to take a picture of a QR code.");
	}