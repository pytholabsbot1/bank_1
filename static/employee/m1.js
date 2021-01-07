a = 2;
var sc , dt;
window.onload = function() {
    console.log( "ready!1" );
    console.log("started2");
    $('#id_maturity_date').attr("readonly","readonly");

    $('select[name ="scheme"]').on('change', function() {
        sc =  $('select[name ="scheme"] option:selected').text().split(" ");
        
        if(sc[1] != "None"){

            date_test = $(".field-account_opening_date .readonly").text().split(",");
            dt = new Date(date_test[0] + ', ' + date_test[1]);
            if(sc[2]=="days"){
                console.log("days");
                dt.setDate( dt.getDate() + parseInt(sc[1]) );
            
            }else if(sc[2]=="months"){
                console.log("months");
                dt.setMonth( dt.getMonth() + parseInt(sc[1]) );
            
            }else{
                console.log("years");
                var y = dt.getFullYear();
                dt.setFullYear(y + parseInt(sc[1]) );
            }
    
            var date = dt.getDate();
            var month = dt.getMonth()+1;
    
            if (date<10) date = '0'+date ;
            if (month<10) month = '0'+month ;
    
            $('input[name ="maturity_date"]').val( dt.getFullYear() + '-' + month +'-' + date);
    console.log("TEST m1")
        }
      });
};