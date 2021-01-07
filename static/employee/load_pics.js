window.onload = function(){
    $("#id_available_amount").attr('readonly', 'readonly');
    $('#id_holder_name').attr("readonly","readonly");
    $('#id_society_account').attr("readonly","readonly");
    $("#content").prepend(`<div style="margin-top: 20px;margin-bottom: 20px;"> 
    <button onclick="load_()">Load Details</button></div>`);

    var photo = window.location.href.split("?")[1].split("=")[2].split("&")[0];
    var sign = window.location.href.split("?")[1].split("=")[3].split("&")[0];
    
    console.log(sign, photo);
    $(".field-image_tag").append(`<img src="/media/users/images/${photo}" alt="" style="width: 100px;">`);
    $(".field-sign_tag").append(`<img src="/media/users/images/${sign}" alt="" style="width: 100px;">`);
};



function load_(){
    $.get( "/bank/wd_comps/" + $("#id_society_account").val() , function( data ) {
        d_ = data.split(',');

        $("#id_holder_name").val(d_[0]);
        $("#id_available_amount").val(d_[1]);

        if($("#id_category").val()!="withdraw"){
            $("#id_intrest_amount").val(d_[2]);
        }else{
            $("#id_intrest_amount").val(0);
        }
        
        $(".field-image_tag").append(`<img src="/media/users/images/${d_[3]}" alt="" style="width: 100px;">`);

        $(".field-sign_tag").append(`<img src="/media/users/images/${d_[4]}" alt="" style="width: 100px;">`);
         
    });
}