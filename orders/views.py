from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from django.urls import reverse
from instamojo_wrapper import Instamojo
from django.http import HttpResponse, HttpResponseRedirect
from .models import Order, OrderItem
from django.template.loader import render_to_string
import weasyprint
from django.conf import settings


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                a=OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            price=OrderItem.get_cost(a)
            # clear the cart
            request.session['order_id'] = order.id
            cart.clear()
            api = Instamojo(api_key="327dc26252b623af6faa0ef987188be5", auth_token="fb79872dab2032fd4c678f4d927c5625", endpoint='https://test.instamojo.com/api/1.1/');
            response = api.payment_request_create(
                purpose= 'Review Hub',
                amount= price,
                buyer_name= order.get_full_name(),
                email= order.email,
                phone= order.mobile,
                redirect_url=request.build_absolute_uri(reverse('orders:invoice', kwargs={'order_id':order.id})),
                send_email= 'True',
                send_sms= 'True',
                webhook= 'http://www.example.com/webhook/',
                allow_repeated_payments= 'False',
            )
            print (response)
            return HttpResponseRedirect(response['payment_request']['longurl'])
            # launch asynchronous task
            #order_created.delay(order.id)
            #return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})

def invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    #return render(request, 'orders/order/pdf.html', {'order': order})
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    return response
