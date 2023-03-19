function startPayment(amount) {
    // Create the checkout configuration object
    var options = {
      "key": "rzp_test_FznCc4xn53Y0R9",
      "amount": amount,
      "currency": "INR",
      "name": "See and wear Footwears",
      "description": "Thank you for purchasing with Happy Feetz. See you Soon",
      "image": "your_logo_url",
      "handler": function (response){
        // Handle the payment response
        handlePaymentResponse(response);
      },
      "prefill": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "contact": "+919876543210"
      },
      "notes": {
        "shipping_address": "123 Shipping St, Shipping City",
        "billing_address": "456 Billing St, Billing City"
      },
      "theme": {
        "color": "#F37254"
      }
    };
  
    // Create the Razorpay checkout object and open it
    var rzp1 = new Razorpay(options);
    rzp1.open();
  }
  