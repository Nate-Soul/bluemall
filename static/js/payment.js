$(function(){
    $("input[type=radio][name=delivery_option]").on("change", function(e){
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/payment/update_basket_delivery/",
            data: {
                delivery_option: parseInt($(this).val()),
                csrfmiddlewaretoken: token,
                action: "post",
            },
            success: function(json){
                $("#total").text(json.final_price)
                $("#deliveryFee").text(json.delivery_fee)
            },
            error: function(xhr, msg, error){
                alert(msg +': '+error);
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function initPaypalButton(){
    paypal.Buttons({
        style: {
            layout:  'vertical',
            color:   'blue',
            shape:   'pill',
            label:   'paypal'
        },
        // Sets up the transaction when a payment button is clicked
        createOrder: function(data, actions) {
            return actions.order.create({
            purchase_units: [{
                amount: {
                value: FINAL_PRICE // Can reference variables or functions. Example: `value: document.getElementById('...').value`
                }
                }]
            });
        },
        // Finalize the transaction after payer approval
        onApprove: function(data) {
            var crsftoken = getCookie('csrftoken');
            var EXECUTE_URL = "http://127.0.0.1:8000/payment/complete/";
            return fetch(EXECUTE_URL, {
                method: "POST",
                headers: {
                    'content-type': 'application/json',
                    'X-CSRFToken': crsftoken,
                },
                body: JSON.stringify({
                   'orderID': data.orderID
                })
            }).then(function(orderData) {
                location.href = 'http://127.0.0.1:8000/payment/successful/';
            });
    }
    }).render('#paypal-button-container');
}

initPaypalButton();