$(function(){

    $("#placeOrderBtn").on("click", function(e){
        e.preventDefault();
        var CSRF_TOKEN = $("input[name='csrfmiddlewaretoken']").val();
        var full_name  = ($("#id_full_name").val() == '') ? "John Doe" : $("#id_full_name").val();
        var address_1  = ($("#id_address_1").val() == '') ? "Address 1" : $("#id_address_1").val();
        var address_2  = ($("#id_address_2").val() == '') ? "Address 2" : $("#id_address_2").val();
        var city       = ($("#id_city").val() == '') ? "Uyo" : $("#id_city").val();
        var phone      = ($("#id_phone").val() == '') ? "234 555 666 7777" : $("#id_phone").val();
        var post_code  = ($("#id_post_code").val() == '') ? 111111 : $("#id_post_code").val();
        var order_key  = Number(new Date());
        $.ajax({
            type: "POST",
            url: "/orders/add/",
            data: {
                full_name: full_name,
                address_1: address_1,
                address_2: address_2,
                city: city,
                phone: phone,
                post_code: post_code,
                order_key: order_key,
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: "add",
            },
            success: function(){
                window.location.href = '/payment/orderplaced/';
            },
            error: function(){
                alert('order failed!');
            }
        })
    });

});