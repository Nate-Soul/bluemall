$(function(){

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

    //convert to positive integer
    function convert_to_pint(a){
        a = parseInt(a);
        if ( isNaN(a) ){
            a = 1;
        } else if (a < 0) {
            a = a * -1;
        } else if(a == 0){
            a = 1;
        }
        return a;
    }


    //add to cart
    $("#addToCartBtn").on("click", function(event){
        event.preventDefault();
        var addBtn = $(this);
        var product_id = addBtn.val();
        var product_qty = $("#selectQty option:selected").val();
        addItemsToCart(product_id, product_qty);
    });

    if($(".add-to-cart-btn").length > 0){
        $(".add-to-cart-btn").each(function(){
            $(this).on("click", function(event){
                event.preventDefault();
                var cart_btn = $(this);
                var product_id = cart_btn.data("index");
                var product_qty = 1;
                addItemsToCart(product_id, product_qty);
            });
        });   
    }

    //add items to cart function
    function addItemsToCart(id, qty){
        var token = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/cart/add/',
            data: {
                productId: id,
                productQty: qty,
                csrfmiddlewaretoken: token,
                action: 'add',
            },
            success: function(json){
                $("#cartItems").text(json.qty);
                alert(qty+" item(s) added to cart");
            },
            error: function(xhr, msg, error){
                alert(msg+": "+error);
            }
        });
    }

    
    //add qty
    if((".btn-qty-plus").length > 0){
        $(".btn-qty-plus").each(function(){
            $(this).on("click", function(event){
                event.preventDefault();
                var x = $(this).siblings(".product-qty-field");
                var product_qty = convert_to_pint(x.val());
                if(product_qty >= 1){
                    product_qty += 1;
                }
                x.val(product_qty);
                var product_id = parseInt($(this).data("index"));
                updateCartItems(product_id, product_qty);
            });
        });    
    }
    
    
    //subtract qty
    if((".btn-qty-minus").length > 0){
        $(".btn-qty-minus").each(function(){
            $(this).on("click", function(event){
                event.preventDefault();
                var x = $(this).siblings(".product-qty-field");
                var y = x.val();
                var product_qty = convert_to_pint(y);
                if(product_qty > 1){
                    product_qty -= 1;
                }
                x.val(product_qty);
                var product_id = parseInt($(this).data("index"));
                updateCartItems(product_id, product_qty);
            });
        });
    }


    //init binding function
    if($(".product-qty-field").length > 0){
        $(".product-qty-field").each(function(){
            var input = $(this);
            input.on("keydown", function(e){
                if(e.which == 13){
                    var product_id = input.siblings(".btn-qty-minus").data("index");
                    var product_qty = input.val();
                    var product_qty = convert_to_pint(product_qty);
                    input.val(product_qty);
                    updateCartItems(product_id, product_qty);
                }
            });
        });
    }
    

    //update cart ajax request
    function updateCartItems(id, qty){
        var CSRF_TOKEN = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/cart/update/',
            data: {
                productId: id,
                productQty: qty,
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: 'update'
            },
            success: function(json){
                $("#cartItems").text(json.qty);
                $("#totalPrice"+ id + " span").text(json.total);
                $("#subTotal span").text(json.sub_total)
                alert('cart updated');
            },
            error: function(xhr, error_msg, error){
                alert('An error occurred: '+error_msg);
            }
        });
    }


    //delete item from cart
    $(".del-from-cart-btn").each(function(){
        var removeBtn = $(this);
        var product_id = removeBtn.data("index");
        var CSRF_TOKEN = getCookie('csrftoken');
        //var csrf_t = $("input[name='token']").val();
        removeBtn.on("click", function(event){
            event.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/cart/delete/',
                data: {
                    productId: product_id,
                    csrfmiddlewaretoken: CSRF_TOKEN,
                    action: 'delete',
                },
                success: function(json){
                    $("#cart-tr"+product_id).remove();
                    $("#cartItems").text(json.qty);
                    $("#subTotal span").text(json.sub_total);
                    alert('item(s) removed from cart');
                },
                error: function(xhr, error_msg, error){
                    alert(error+": "+error_msg);
                }
            });
        });
    });


});