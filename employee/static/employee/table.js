$(document).ready(function (){
    var pathname = window.location.pathname.split("/").pop();
    var accounts = ['withdrawls', 'loans', 'maturity', 'emi_due'];
    var employees = ['daily_report_dp', 'daily_report_fc', 'daily_cash'];
    var finances = ['document_dispatch']
    if (accounts.includes(pathname)){
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
    
            $("#id_search").select2({ data: sampleArray });
        });
    }
    if (employees.includes(pathname)){
        $.get('/bank/emp_data', function(data){
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
    
            $("#id_search").select2({ data: sampleArray });
        });
    }
    if (finances.includes(pathname)){
        $.get('/bank/doc_data/all_loans', function(data){
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
    
            $("#id_search").select2({ data: sampleArray });
        });
    }
    // $.get('/bank/emp_data/', function(data){
    //     var data_json = JSON.parse(data);
    //     var sampleArray = [];
    //     for (var i=0; i < data_json.data.dlist_1.length; i++){
    //         var pk = data_json.data.dlist_1[i];
    //         var nom_num = data_json.data.dlist_2[i];
    //         var name = data_json.data.dlist_3[i];
    //         dataobject = {
    //             id: pk,
    //             text: pk + ' - ' + name + ' - ' + nom_num
    //         };
    //         sampleArray.push(dataobject);
    //     }

    //     $("#id_acc_num").select2({ data: sampleArray });
    // });
});