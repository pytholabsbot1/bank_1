
$(document).ready(function (){
    $("#e10").hide();
    $("#object").hide();
    $("#print").hide();
    $("#history").hide();
    $("#print-history").hide();
    $("body > form > div > div > div > div.spinner.m-4").hide();
    
    $("#docsubmit").click(function(){
        $("body > form > div > div > div > div.spinner.m-4").show();
        var doc_string = $("#selectdocument").val();
        $.get('/bank/doc_data/' + doc_string, function(data){
            var data_json = JSON.parse(data);
            console.log(data_json);
            console.log(data_json.data);
            var sampleArray = [];
            for (var i=0; i < data_json.data.dlist_1.length; i++){
                var pk = data_json.data.dlist_1[i];
                var nom_num = data_json.data.dlist_2[i];
                var name = data_json.data.dlist_3[i];
                dataobject = {
                    id: `/bank/transit/${data_json.tp}/${pk}`,
                    text: pk + ' - ' + name + ' - ' + nom_num
                };
                sampleArray.push(dataobject);
            }

            $("#e10").select2({ data: sampleArray });
            $("#object").show();
        });
        setTimeout(function(){ console.log("Hello"); }, 3000);
        $("body > form > div > div > div > div.spinner.m-4").hide();
        $("#docsubmit").hide();
        $("#selectdocument").attr('disabled', 'disabled');
      });
      $("#object").click(function(){
        $("#object").hide();
        var url = $("#e10").val();
        $("#print").attr('href', url);
        $("#print").show();
        $("#history").show();
    });
    $("#history").click(function(){
        var pk = $("#e10").val();
        var info = pk.split('/');
        $.get(`/bank/print_data/${info[3]}/${info[4]}`, function(data){
            var new_json = JSON.parse(data);
            $("#print-history").show();
            $('#print-history').dataTable({
                "aaData": new_json,
                "aoColumns": [
                    { "mDataProp": "index" },
                    { "mDataProp": "user" },
                    { "mDataProp": "timestamp" }
                ]
            });
        });
    })
});