
$(document).ready(function (){
    if (!$) {
        $ = django.jQuery;
    }
    $("#account-type").hide();
    $("#account-select").hide();
    $("#submit").hide();
    $(".dates").hide()
    // $("#dep_search").hide();
    // $("#fc_search").hide();
    $("input[name='type']").change(function(e){
        $("#acc_search").empty();
        if($(this).val() == 'account') {
            $("#account-type").show();
            $.get('/bank/doc_data/client', function(data){
                var data_json = JSON.parse(data);
                var sampleArray = [];
                for (var i=0; i < data_json.data.dlist_1.length; i++){
                    var pk = data_json.data.dlist_1[i];
                    var nom_num = data_json.data.dlist_2[i];
                    var name = data_json.data.dlist_3[i];
                    dataobject = {
                        id: pk,
                        text: pk + ' - ' + name + ' - ' + nom_num
                    };
                    sampleArray.push(dataobject);
                }
                $("#acc_search").select2({ data: sampleArray });
                $("#account-select").show();
                $("#submit").show();
                $(".dates").show();
            });
        }
        if($(this).val() == 'employee') {
            $("#account-type").hide();
            $.get('/bank/emp_data/', function(data){
                var data_json = JSON.parse(data);
                var sampleArray = [];
                for (var i=0; i < data_json.data.dlist_1.length; i++){
                    var pk = data_json.data.dlist_1[i];
                    var nom_num = data_json.data.dlist_2[i];
                    var name = data_json.data.dlist_3[i];
                    dataobject = {
                        id: pk,
                        text: pk + ' - ' + name + ' - ' + nom_num
                    };
                    sampleArray.push(dataobject);
                }
                $("#acc_search").select2({ data: sampleArray });
                $("#account-select").show();
                $("#submit").show();
                $(".dates").show();
            });
        }
    });
});