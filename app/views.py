from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.http import HttpResponse
from .models import Order, OrderItem
from django import forms
from django.db.models import F

class OrderItemForm(forms.Form):
    item_name = forms.CharField(max_length=255)
    quantity = forms.IntegerField(min_value=1)

def create_order(request):
    if request.method == 'POST':
        order = Order.objects.create()
        return redirect('add_items', order_id=order.unique_id)
    return render(request, 'app/create_order.html')

def add_items(request, order_id):
    order = get_object_or_404(Order, unique_id=order_id)
    OrderItemFormSet = formset_factory(OrderItemForm, extra=1)
    
    if request.method == 'POST':
        formset = OrderItemFormSet(request.POST)
        if formset.is_valid():
            for form in formset.cleaned_data:
                if form:  # Check if the form is not empty
                    item = OrderItem.objects.filter(order=order,item_name=form['item_name']).first()
                    if item :
                        item.quantity = F("quantity") + form['quantity']
                        item.save()
                    else:
                        OrderItem.objects.create(
                            order=order,
                            item_name=form['item_name'],
                            quantity=form['quantity']
                        )
            return redirect('order_details', order_id=order_id)
    else:
        formset = OrderItemFormSet()
    
    return render(request, 'app/add_items.html', {
        'formset': formset,
        'order': order
    })

def order_details(request, order_id):
    order = get_object_or_404(Order, unique_id=order_id)
    items = order.items.all()
    return render(request, 'app/order_details.html', {
        'order': order,
        'items': items
    })
