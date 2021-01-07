
$(document).ready(function (){
    if (!$) {
        $ = django.jQuery;
    }
    if ($("#id_TYPE").val() == "Other") {
        $(".field-type_other").show();
        $("#id_type_other").attr("placeholder", "other type document info here");
    }
    else {
        $(".field-type_other").hide();
    }
    $( "#id_TYPE" ).change(function() {
        if (this.value == "Other") {
            $(".field-type_other").show();
            $("#id_type_other").attr("placeholder", "other type document info here");
        }
        else {
            $(".field-type_other").hide();
        }
    });

    var hashParams = window.location.hash.substr(1);
	hashParams = atob(hashParams);
    hashParams = hashParams.split('&');
    console.log(hashParams);
	// console.log(typeof(hashParams))
    if (hashParams[0]){
		for(var i = 0; i < hashParams.length; i++){
			var p = hashParams[i].split('=');
            document.getElementById(p[0]).value = decodeURIComponent(p[1]);
        }
    }
});