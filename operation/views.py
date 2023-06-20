from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from PyPDF2 import PdfWriter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.http import FileResponse
from .forms import ClaimForm

# Create your views here.

def index_page(request):
    return render(request, 'index.html')

def order_page(request, order_id="0"):
    if order_id != "0":
        order = Order.objects.get(order_id=order_id)
        order_products = OrderProduct.objects.filter(order_id=order_id)

        total = 0
        for p in order_products:
            total += (p.product.price * p.quantity)

        return render(request, 'order.html', {
            'order': order,
            'order_products': order_products,
            'total': total
            })
    print("holas")
    return render(request, 'order.html', {'order': order_id})

def payment_page(request):
    return render(request, 'payment.html')

def delivery_page(request):
    return render(request, 'delivery.html')

# def complaints_page(request):
#     return render(request, 'complaints.html')

def product_page(request, barcode, order_id=0):
    product = Product.objects.get(barcode=barcode)
    return render(request, 'product.html', {
        'product': product,
        'order': order_id
        })

def add_product(request):
    if request.method == 'POST':
        order_id = request.POST['order']
        barcode = request.POST['barcode']
        quantity = request.POST['quantity']
        product = Product.objects.get(barcode=barcode)

        order_route = f"/order/order_id={order_id}" if order_id != "0" else "/order"

        if product.stock < int(quantity):
            messages.error(request, f'Stock insuficiente. Disponible: {product.stock}')
            return redirect(f'{order_route}/product={barcode}')
        else:
            if order_id == "0":
                order = Order.objects.create()
                order.save()
                order_id = order.order_id

            product.stock -= int(quantity)
            product.save()
            order_product = OrderProduct.objects.create(order_id=order_id, 
                                                        product_id=product.id, 
                                                        quantity=quantity)
            order_product.save()
            order_route = f"/order/order_id={order_id}"
            return redirect(order_route)
    else:
        return HttpResponse('Método inválido')
    
def cancel_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order.status = "Anulado"
    order.save()

    order_products = OrderProduct.objects.filter(order_id=order_id)

    for p in order_products:
        product = Product.objects.get(id=p.product_id)
        product.stock += p.quantity
        product.save()

    return redirect(f"/order")
    
def confirm_order(request, order_id):
    order = Order.objects.get(order_id=order_id)

    order.status = "Confirmado"
    order.save()
    return redirect(f"/order/order_id={order_id}/voucher")

def gen_pdf(request, order):
    import barcode
    from barcode.writer import ImageWriter

    order = Order.objects.get(order_id=order)
    order_number = str(order.order_id).zfill(10)

    from datetime import datetime
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    
    order_products = OrderProduct.objects.filter(order_id=order.order_id)
    total = 0
    for p in order_products:
        total += (p.product.price * p.quantity)

    # barcode
    barcode_filename = f"{order_number}"
    barcode_format = barcode.get_barcode_class('code128')
    my_barcode = barcode_format(order_number, writer=ImageWriter())
    my_barcode.save(barcode_filename)


    # data
    data = f"""
    Orden: {order_number}   
    Fecha: {date}
    Hora: {time}    
    Total: ${total}                
    """

    # pdf
    filename = f"{order_number}.pdf"
    c = canvas.Canvas(filename)

    c.setFont("Helvetica", 12)
    c.drawString(100, 700, data)
    c.drawImage(f"{barcode_filename}.png", 100, 600, width=100, height=50)

    c.showPage()
    c.save()


    response = FileResponse(open(filename, "rb"))
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    import os
    try:
        os.remove(f"{barcode_filename}.png")
        os.remove(f"{filename}")
    except:
        pass

    return response

def claim_add(request):

     template_name = 'complaints.html'

     data = {
        'form': ClaimForm()
    }

     if request.method == 'POST':
         form = ClaimForm(data=request.POST, files=request.FILES)
         if form.is_valid():
             form.save()
             data["msg"] = "Reclamo guardado"
         else:
             data["form"] = form

     return render(request, template_name, data)

def claim_list(request):
    template_name = 'complaints_list.html'

    data = {
        'claims': Claim.objects.all()
    }

    return render(request, template_name, data)