from http import HTTPStatus

import stripe

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from orders.forms import OrderForm
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.conf import settings
from django.urls.base import reverse,reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from products.models import Basket
from orders.models import Order


from user.common import TitleMixin
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_KEY


class SuccessView(TitleMixin,TemplateView):
    title = 'Store - спасибо за заказ'
    template_name = 'orders/success.html'

class CancelTemplateView(TitleMixin,TemplateView):
    template_name = 'orders/cancel.html'

class OrderListView(TitleMixin,ListView):
    template_name = 'orders/orders.html'
    title = 'Store - заказы'
    queryset = Order.objects.all()
    ordering = ('-created')
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)

class OrderDetailView(TitleMixin,DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Store - заказ#{self.object.id}'
        return context

class OrderCreateView(TitleMixin,CreateView):
    form_class = OrderForm
    template_name = 'orders/order-create.html'
    success_url = reverse_lazy('orders:order-create')
    title = 'Store - оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items = baskets.stripe_products(),
            metadata = {'order_id': self.object.id},
            mode='payment',
            success_url= f'{settings.DOMAIN_NAME}{reverse("orders:order-success")}',
            cancel_url= f'{settings.DOMAIN_NAME}{reverse("orders:order-cancel")}',
        )
        return HttpResponseRedirect(checkout_session.url,status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


def fulfill_checkout(session_id):
    print("Fulfilling Checkout Session", session_id)

    # TODO: Make this function safe to run multiple times,
    # even concurrently, with the same session ID

    # TODO: Make sure fulfillment hasn't already been
    # peformed for this Checkout Session

    # Retrieve the Checkout Session from the API with line_items expanded
    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )

    # Check the Checkout Session's payment_status property
    # to determine if fulfillment should be peformed
    if checkout_session.payment_status != 'unpaid':
        order = Order.objects.get(id=checkout_session.metadata['order_id'])
        order.update_after_payment()


    #TODO: Perform fulfillment of the line items

    #TODO: Record/save fulfillment status for this
    # Checkout Session


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object']['id'])


    return HttpResponse(status=200)
