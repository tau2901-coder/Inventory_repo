from django.shortcuts import render,redirect
from testapp.models import item_mstr,unit_mstr,brand_mstr,tbl_purchase_mstr,tbl_purchase_details,tbl_sales_master,table_sales_details
from testapp.forms import item_mstr_form,unit_mstr_form,brand_mstr_form,RegistrationForm,tbl_purchase_mstr_form,tbl_purchase_details_form,tbl_sales_master_form,table_sales_details_form,purchase_report_form,sales_report_form
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth
from django.db import transaction
from testapp.models import generate_invoice_no
from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'testapp/home.html')

@login_required(login_url='login')
def user_detail(request):
    return render(request,"testapp/user_detail.html")

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/user_detail')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, 'testapp/change_password.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect( '/home' )
    else:
        form = RegistrationForm()
    context = {
             "form":form
         }
    return render(request,'testapp/signup.html',context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            print(username)
            print(password)
            if user is not None:
                auth.login(request, user)
                return redirect('/home')
        # invalid form (wrong username/password) -> fall through with same form + errors
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, 'testapp/login.html', context)

def logout_view(request):
    auth.logout(request)
    return redirect('/home')

@login_required(login_url='login')
def add_item(request):
    if request.method == "POST":
        form=item_mstr_form(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.username = request.user
            item.save()
            return redirect("/view_item")
    form = item_mstr_form()
    return render(request,"testapp/add_item.html",{"form":form})

@login_required(login_url='login')
def view_item(request):
    obj=item_mstr.objects.filter(status=True)
    return render(request,'testapp/view_item.html',{"obj":obj})

def edit_item(request,id):
    item=item_mstr.objects.get(id=id)
    if request.method =="POST":
        form=item_mstr_form(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect("/view_item")
    form=item_mstr_form(instance=item)
    return render(request,"testapp/edit_item.html",{"form":form})

def delete_item(request,id):
    item=item_mstr.objects.get(id=id)
    item.status=False
    item.save()
    return redirect("/view_item")

#------------Unit----------------------

@login_required(login_url='login')
def view_unit(request):
    obj=unit_mstr.objects.filter(status=True)
    return render(request,"testapp/view_unit.html",{"obj":obj})

def add_unit(request):
    if request.method == "POST":
        form=unit_mstr_form(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.username = request.user
            unit.save()
            return redirect('/view_unit')
    form=unit_mstr_form()
    return render(request,"testapp/add_unit.html",{"form":form})

def edit_unit(request,id):
    unit=unit_mstr.objects.get(id=id)
    if request.method =="POST":
        form=unit_mstr_form(request.POST,instance=unit)
        if form.is_valid():
            form.save()
            return redirect("/view_unit")
    form=unit_mstr_form(instance=unit)
    return render(request,"testapp/edit_unit.html",{"form":form})

def delete_unit(request,id):
    unit=unit_mstr.objects.get(id=id)
    unit.status=False
    unit.save()
    return redirect('/view_unit')

#-----------------------brand------------------------------
@login_required(login_url='login')
def brand_view(request):
    obj=brand_mstr.objects.filter(status=True)
    return render(request,"testapp/brand_view.html",{"obj":obj})

def add_brand(request):
    if request.method=="POST":
        form=brand_mstr_form(request.POST)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.username = request.user
            brand.save()
            return redirect('/brand_view')
    form=brand_mstr_form()
    return render(request,"testapp/add_brand.html",{"form":form})

def edit_brand(request,id):
    brand=brand_mstr.objects.get(id=id)
    if request.method == "POST":
        form=brand_mstr_form(request.POST,instance=brand)
        if form.is_valid():
            form.save()
            return redirect('/brand_view')
    form=brand_mstr_form(instance=brand)
    return render(request,"testapp/edit_brand.html",{"form":form})

def delete_brand(request,id):
    brand=brand_mstr.objects.get(id=id)
    brand.status=False
    brand.save()
    return redirect("/brand_view")

#-----------Purchase--------------------------

def view_purchase_mstr(request  ):
    obj=tbl_purchase_mstr.objects.filter(status=True)
    #total_amount=tbl_purchase_mstr.objects.filter(total_amount=total_amount)
    return render(request,"testapp/view_purchase_mstr.html",{"obj":obj})

def edit_purchase_mstr(request,id):
    pur_mstr=tbl_purchase_mstr.objects.get(id=id)
    if request.method == "POST":
        form=tbl_purchase_mstr_form(request.POST,instance=pur_mstr)
        if form.is_valid():
            form.save()
            return redirect('/view_purchase_mstr')
    form=tbl_purchase_mstr_form(instance=pur_mstr)
    return render(request,"testapp/edit_purchase_mstr.html",{"form":form})

def delete_purchase_mstr(request,id):
    pur_mstr=tbl_purchase_mstr.objects.get(id=id)
    pur_mstr.status=False
    pur_mstr.save()
    return redirect('/view_purchase_mstr')

#-------------------------Purchase Details--------------------------

def view_purchase_details(request):
    masters = tbl_purchase_mstr.objects.filter(status=True).order_by('-datetime')
    grouped = []
    for m in masters:
        details = m.tbl_purchase_details_set.filter(status=True)
        items = []
        total = 0
        for d in details:
            base_amount = d.rate * d.quantity
            gst_amount = d.amount - base_amount
            items.append({
                "id": d.id,
                "item_name": d.item_id.name,
                "rate": d.rate,
                "quantity": d.quantity,
                "base_amount": base_amount,
                "gst_amount": gst_amount,
                "amount": d.amount,
            })
            total += d.amount
        grouped.append({"master": m, "items": items, "total": total})
    return render(request, "testapp/view_purchase_details.html", {"grouped": grouped})



def view_purchase_detail_single(request, id):
    master = tbl_purchase_mstr.objects.get(id=id, status=True)
    details = master.tbl_purchase_details_set.filter(status=True)
    items = []
    grand_total = 0
    for d in details:
        base_amount = d.rate * d.quantity
        gst_amount = d.amount - base_amount
        items.append({
            "id": d.id,
            "item_name": d.item_id.name,
            "rate": d.rate,
            "quantity": d.quantity,
            "base_amount": base_amount,
            "gst_amount": gst_amount,
            "amount": d.amount,
        })
        grand_total += d.amount
    return render(request, "testapp/view_purchase_detail_single.html", {
        "master": master,
        "items": items,
        "grand_total": grand_total,
    })


def get_item_available_stock(item_id):
    """Total purchased qty minus total sold qty for an item - live stock, purchase/sale records se seedhe calculate."""
    purchased = tbl_purchase_details.objects.filter(item_id=item_id, status=True).aggregate(total=Sum('quantity'))['total'] or 0
    sold = table_sales_details.objects.filter(item_id=item_id, status=True).aggregate(total=Sum('quantity'))['total'] or 0
    return purchased - sold


def add_purchase_full(request):
    items = item_mstr.objects.filter(status=True)

    if request.method == "POST":
        invoice_no = request.POST.get('invoice_no')
        invoice_date = request.POST.get('invoice_date')
        name = request.POST.get('name')
        contact_no = request.POST.get('contact_no')

        item_ids = request.POST.getlist('item_id[]')
        quantities = request.POST.getlist('quantity[]')
        gst_input = request.POST.get('gst', 18)
        try:
            selected_gst = float(gst_input)
        except (TypeError, ValueError):
            selected_gst = None

        errors = []
        if not invoice_no:
            errors.append("Invoice No missing hai.")
        if not invoice_date:
            errors.append("Invoice Date daalo.")
        if not name:
            errors.append("Supplier Name daalo.")
        if not item_ids:
            errors.append("Kam se kam ek item add karo.")
        if selected_gst not in (12, 15, 18):
            errors.append("GST 12%, 15% ya 18% me se choose karo.")

        if not errors:
            with transaction.atomic():
                purchase = tbl_purchase_mstr.objects.create(
                    invoice_no=int(invoice_no),
                    invoice_date=invoice_date,
                    name=name,
                    contact_no=contact_no,
                    username=request.user.username,
                    total_amount=0,
                    gst=selected_gst,
                )

                added_amount = 0
                saved_items = []
                for i in range(len(item_ids)):
                    item_obj = item_mstr.objects.get(id=item_ids[i])
                    qty = int(quantities[i])
                    detail = tbl_purchase_details.objects.create(
                        purcahse_mstr_id=purchase,
                        item_id_id=item_obj.id,
                        quantity=qty,
                        gst=selected_gst,
                        rate=item_obj.rate,
                        amount=0,
                        username=request.user.username,
                    )
                    added_amount += detail.amount
                    base_amount = detail.rate * detail.quantity
                    saved_items.append({
                        "item_name": item_obj.name,
                        "quantity": detail.quantity,
                        "rate": detail.rate,
                        "base_amount": base_amount,
                        "gst_amount": detail.amount - base_amount,
                        "amount": detail.amount,
                    })

                purchase.total_amount = round(added_amount)
                purchase.save()

            return render(request, "testapp/add_purchase_full.html", {
                "items": items,
                "success_invoice_no": purchase.invoice_no,
                "success_name": purchase.name,
                "success_contact": purchase.contact_no,
                "success_date": purchase.invoice_date,
                "success_items": saved_items,
                "success_total": purchase.total_amount,
            })

        return render(request, "testapp/add_purchase_full.html", {
            "items": items,
            "errors": errors,
            "default_invoice_no": invoice_no or generate_invoice_no(),
        })

    return render(request, "testapp/add_purchase_full.html", {
        "items": items,
        "default_invoice_no": generate_invoice_no(),
    })


def edit_purchase_details(request,id):
    pur=tbl_purchase_details.objects.get(id=id)
    if request.method == "POST":
        form=tbl_purchase_details_form(request.POST,instance=pur)
        if form.is_valid():
            form.save()
            return redirect('/view_purchase_deatils')
    form=tbl_purchase_details_form(instance=pur)
    return render(request,"testapp/edit_purchase_details.html",{"form":form})


def delete_purchase_details(request,id):
    pur_detl=tbl_purchase_details.objects.get(id=id)
    pur_detl.status=False
    pur_detl.save()
    return redirect('/view_purchase_deatils')

#---------------Sales Master----------------------

def view_sales_master(request):
    obj=tbl_sales_master.objects.filter(status=True)
    return render(request,"testapp/view_sales_master.html",{"obj":obj})


def edit_sales_master(request,id):
    sale=tbl_sales_master.objects.get(id=id)
    if request.method =="POST":
        form=tbl_sales_master_form(request.POST,instance=sale)
        if form.is_valid():
            form.save()
            return redirect('/view_sales_master')
    form=tbl_sales_master_form(instance=sale)
    return render(request,"testapp/edit_sales_master.html",{"form":form})

def delete_sales_master(request,id):
    sale=tbl_sales_master.objects.get(id=id)
    sale.status=False
    sale.save()
    return redirect('/view_sales_master')

def merge_purchase_mstr_details(request):pass

#-----------------Sales Details------------------


def view_sales_details(request):
    masters = tbl_sales_master.objects.filter(status=True).order_by('-datetime')
    grouped = []
    for m in masters:
        details = m.table_sales_details_set.filter(status=True)
        items = []
        total = 0
        for d in details:
            base_amount = d.rate * d.quantity
            gst_amount = d.amount - base_amount
            items.append({
                "id": d.id,
                "item_name": d.item_id.name,
                "rate": d.rate,
                "quantity": d.quantity,
                "base_amount": base_amount,
                "gst_amount": gst_amount,
                "amount": d.amount,
            })
            total += d.amount
        grouped.append({"master": m, "items": items, "total": total})
    return render(request, "testapp/view_sales_details.html", {"grouped": grouped})




def view_sales_detail_single(request, id):
    master = tbl_sales_master.objects.get(id=id, status=True)
    details = master.table_sales_details_set.filter(status=True)
    items = []
    grand_total = 0
    for d in details:
        base_amount = d.rate * d.quantity
        gst_amount = d.amount - base_amount
        items.append({
            "id": d.id,
            "item_name": d.item_id.name,
            "rate": d.rate,
            "quantity": d.quantity,
            "base_amount": base_amount,
            "gst_amount": gst_amount,
            "amount": d.amount,
        })
        grand_total += d.amount
    return render(request, "testapp/view_sales_detail_single.html", {
        "master": master,
        "items": items,
        "grand_total": grand_total,
    })


"""def view_sales_details(request):
    obj=table_sales_details.objects.filter(status=True)
    return render(request,"testapp/view_sales_details.html",{"obj":obj})"""

def add_sales_full(request):
    items_qs = item_mstr.objects.filter(status=True)
    items = []
    for it in items_qs:
        items.append({
            "id": it.id,
            "name": it.name,
            "rate": it.rate,
            "stock": get_item_available_stock(it.id),
        })

    if request.method == "POST":
        invoice_no = request.POST.get('invoice_no')
        invoice_date = request.POST.get('invoice_date')
        name = request.POST.get('name')
        contact_no = request.POST.get('contact_no')

        item_ids = request.POST.getlist('item_id[]')
        quantities = request.POST.getlist('quantity[]')
        gst_input = request.POST.get('gst', 18)
        try:
            selected_gst = float(gst_input)
        except (TypeError, ValueError):
            selected_gst = None

        errors = []
        if not invoice_no:
            errors.append("Invoice No Missing.")
        if not invoice_date:
            errors.append("Invoice Date Missing.")
        if not name:
            errors.append("Customer Name Missing.")
        if not item_ids:
            errors.append("Kam se kam ek item add karo.")
        if selected_gst not in (12, 15, 18):
            errors.append("GST 12%, 15% ya 18% me se choose karo.")


        if not errors:
            required_qty = {}
            for i in range(len(item_ids)):
                required_qty[item_ids[i]] = required_qty.get(item_ids[i], 0) + int(quantities[i])
            for iid, req_qty in required_qty.items():
                item_obj = item_mstr.objects.get(id=iid)
                available = get_item_available_stock(iid)
                if available < req_qty:
                    errors.append(
                        f"Not enough stock for {item_obj.name}. Available: {available}, Required: {req_qty}."
                    )

        if not errors:
            with transaction.atomic():
                sale = tbl_sales_master.objects.create(
                    invoice_no=int(invoice_no),
                    invoice_date=invoice_date,
                    name=name,
                    contact_no=contact_no,
                    username=request.user.username,
                    total_amount=0,
                    gst=selected_gst,
                )

                added_amount = 0
                saved_items = []
                for i in range(len(item_ids)):
                    item_obj = item_mstr.objects.get(id=item_ids[i])
                    qty = int(quantities[i])
                    detail = table_sales_details.objects.create(
                        sales_mstr_id=sale,
                        item_id_id=item_obj.id,
                        quantity=qty,
                        gst=selected_gst,
                        rate=item_obj.rate,
                        amount=0,
                        username=request.user.username,
                    )
                    added_amount += detail.amount
                    base_amount = detail.rate * detail.quantity
                    saved_items.append({
                        "item_name": item_obj.name,
                        "quantity": detail.quantity,
                        "rate": detail.rate,
                        "base_amount": base_amount,
                        "gst_amount": detail.amount - base_amount,
                        "amount": detail.amount,
                    })

                sale.total_amount = round(added_amount)

            return render(request, "testapp/add_sales_full.html", {
                "items": items,
                "success_invoice_no": sale.invoice_no,
                "success_name": sale.name,
                "success_contact": sale.contact_no,
                "success_date": sale.invoice_date,
                "success_items": saved_items,
                "success_total": sale.total_amount,
            })

        # error hua to jo invoice_no page pe dikh raha tha wahi wapas dikhao,
        # naya random generate mat karo
        return render(request, "testapp/add_sales_full.html", {
            "items": items,
            "errors": errors,
            "default_invoice_no": invoice_no or generate_invoice_no(),
        })

    # GET request: ek naya random invoice_no generate karke field me dikhado
    return render(request, "testapp/add_sales_full.html", {
        "items": items,
        "default_invoice_no": generate_invoice_no(),
    })


def edit_sales_details(request,id):
    sale=table_sales_details.objects.get(id=id)
    if request.method == "POST":
        form=table_sales_details_form(request.POST,instance=sale)
        if form.is_valid():
            form.save()
            return redirect('/view_sales_details')
    form=table_sales_details_form(instance=sale)
    return render(request,"testapp/edit_sales_details.html",{"form":form})

#-------------------Purchase Report----------------

def search_purchase_report(request):
    obj = None
    grand_total = None
    form = purchase_report_form(request.GET or None)
    if request.method == "GET" and request.GET:
        if form.is_valid():
            item = form.cleaned_data.get('item')
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')

            masters = tbl_purchase_mstr.objects.filter(status=True)
            if from_date:
                masters = masters.filter(datetime__date__gte=from_date)
            if to_date:
                masters = masters.filter(datetime__date__lte=to_date)
            masters = masters.order_by('-datetime')

            obj = []
            running_total = 0
            for m in masters:
                details = m.tbl_purchase_details_set.filter(status=True)
                if item:
                    details = details.filter(item_id=item)
                for d in details:
                    row_amount = d.amount or 0
                    unit_obj = d.item_id.unit_id
                    obj.append({
                        "purchase_mstr_id": m.id,
                        "date": m.datetime,
                        "item_name": d.item_id.name,
                        "item_unit_id": unit_obj.unit if unit_obj else "-",
                        "quantity": d.quantity,
                        "amount": row_amount,
                        "current_stock": get_item_available_stock(d.item_id_id),
                    })
                    running_total += row_amount

            grand_total = round(running_total)
        else:
            obj = []
            grand_total = 0
    return render(
        request,
        "testapp/purchase_report.html",
        {"form": form, "obj": obj, "grand_total": grand_total},
    )


def search_sales_report(request):
    obj = None
    grand_total = None
    form = sales_report_form(request.GET or None)
    if request.method == "GET" and request.GET:
        if form.is_valid():
            item = form.cleaned_data.get('item')

            masters = tbl_sales_master.objects.filter(status=True).order_by('-datetime')

            obj = list()
            running_total = 0
            for m in masters:
                details = m.table_sales_details_set.filter(status=True)
                if item:
                    details = details.filter(item_id=item)
                for d in details:
                    row_amount = d.amount or 0
                    unit_obj = d.item_id.unit_id
                    obj.append({
                        "sales_mstr_id": m.id,
                        "date": m.datetime,
                        "item_name": d.item_id.name,
                        "item_unit_id": unit_obj.unit if unit_obj else "-",
                        "quantity": d.quantity,
                        "amount": row_amount,
                        "current_stock": get_item_available_stock(d.item_id_id),
                    })
                    running_total += row_amount

            grand_total = round(running_total)

        else:
            obj = list()
            grand_total = 0
    return render(
        request,
        "testapp/sales_report.html",{"form": form, "obj": obj, "grand_total": grand_total})


def delete_sales_details(request, id):
    sale_detl = table_sales_details.objects.get(id=id)
    sale_detl.status = False
    sale_detl.save()
    return redirect('/view_sales_details')


