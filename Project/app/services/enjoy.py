import stripe

stripe.api_key = "sk_test_51HeLb7GWjRGxBOOYruap689xNCFhMWetmp25MiJz4LGZoJPqSLTCsNhhoqtvt6DW6qKRHf7iiyyZMeRbN61lL6A500O0PzD1vM"

stripe.PaymentIntent.create(
  amount=1000,
  currency='sgd',
  payment_method_types=['card'],
  receipt_email='jenny.rosen@example.com',
)