from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
			# clear the cart
			cart.clear()
			request.session['order_id'] = order.id
			return redirect(reverse('payment:process'))
			#return render(request, 'orders/order/created.html', {'order': order})

		else:
			form = OrderCreateForm()
		return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})