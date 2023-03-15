

    $(document).ready(function () {
        $('.payWithRazorpay').click(function (e) {
            e.preventDefault();
            alert('hello')
             var options = {
                "key": "rzp_test_FznCc4xn53Y0R9", // Enter the Key ID generated from the Dashboard
                //"amount": "{{razorpayTotal}}",
                "amount": "100",
                // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "See and Wear Footwears",
                "description": "See you soon",
                "image": "https://example.com/your_logo",
                //"order_id": "order_Dd3Wbag7QXDuuL", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1 
                "callback_url": "{% url 'orderCompleted' %}",
                "prefill": {
                    "name": "{{order.fullName}}",
                    "email": "{{order.email}}",
                    "contact": "{{order.phone}}"
                },
                "notes": {
                    "address": "{{order.fullAddress}}"
                },
                "theme": {
                    "color": "#3399cc"
                }
                 "handler": function (responsea){
                    alert(responsea.razorpay_payment_id);
                    alert(responsea.razorpay_order_id);
                    alert(responsea.razorpay_signature)
    
                    data = {
                        'payment_mode':'Razorpay',
                        'payment_id':responsea.razorpay_payment_id,
                        'order_no':order_number,
                        'grand_total':grand_total,
                        csrfmiddlewaretoken: token
                    }
                    $.ajax({
                        method: "POST",
                        url: "orderCompleted",
                        data: data,
                        success: function (responsec) {
                            swal(
                                'Congratulations!',
                                responsec.status,
                                'success'
                            ).then((value) => {
                                console.log(order_number)
                                window.location.href = 'order-completed'+'?order_number='+order_number
                                console.log(order_number)
                            });
    
                        }
                    });
                },
            }
    
    
    var rzp1 = new Razorpay(options);
    document.getElementById('rzp-button1').onclick = function(e){
        rzp1.open();
        e.preventDefault();
    };
    });
    }); 
  
    
    
    
    
<script src="https://checkout.razorpay.com/v1/checkout.js"></script> 
<script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script> 
    