from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render
from datetime import date, datetime

from .models import *
from django import template
from .forms import *
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator
import json
from json import JSONEncoder

from django.urls import reverse
# Create your views here.

def index(request):
    products_picked = Product.objects.all().order_by('?')[:4]   #Random selected 4 products
    products_latest = Product.objects.all().order_by('-id')[:4]  # last 4 products
    products_slider = Product.objects.all().order_by('?')[:4]  #first 4 products
    context = {'products_slider': products_slider, 'products_latest': products_latest,'products_picked': products_picked}
    return render(request,'index.html', context)



def product_detail(request,id,slug):
    #query = request.GET.get('q')
    #category = Category.objects.all()

    product = Product.objects.get(pk=id)
    images = Hinhanhsanpham.objects.filter(productid_id=id)
    orderDetails = Orderdetail.objects.filter(productid=id)

    damua = False
    for detail in orderDetails:
        if detail.orderid.taikhoanid == request.user:
            damua = True
            break

    productAttributes = Attributevalue.objects.filter(productid=id)

    #Review Paging
    review_list = Review.objects.filter(productid = id)
    paginator = Paginator(review_list, 4)
    reviews = paginator.page(1)

    #Comment Paging
    comment_list = Productcomment.objects.filter(productid = id)
    commentPaginator = Paginator(comment_list, 3)
    comments = commentPaginator.page(1)
    commentReplys = []

    for comment in comments:
        replys = Productcommentreply.objects.filter(productcommentid = comment)
        commentReplys.extend(list(replys))

    productDiscounts = ProductDiscount.objects.filter(productid=id)

    context = {
    			'product': product,
                'images': images,
                'comments': comments,
                'reviews' : reviews,
                'commentReplys': commentReplys,
                'damua': damua,
                'discounts': productDiscounts,
               }
    # if productAttribute != None:
    #     if request.method == 'POST': #if we select color
    #         variant_id = request.POST.get('variantid')
    #         variant = Variants.objects.get(id=variant_id) #selected product by click color radio
    #         colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
    #         sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
    #         query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
    #     else:
    #         variants = Variants.objects.filter(product_id=id)
    #         colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
    #         sizes = Variants.objects.raw('SEL2ECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
    #         variant =Variants.objects.get(id=variants[0].id)
    #     context.update({'sizes': sizes, 'colors': colors,
    #                     'variant': variant,'query': query
    #                     })

    #-------------------------------------------------------------------
    #--------------------------------------------------------------------------
    # productAttributes = Attributevalue.objects.filter(productid=id)
    # if productAttributes != None:
    #     colors = []
    #     sizes = []
    #     color_size = productAttributes.filter(attributeid__tenthuoctinh = "color-size")
    #     colorAttribute = productAttributes.filter(attributeid__tenthuoctinh = "color")
    #     sizeAttribute = productAttributes.filter(attributeid__tenthuoctinh = "size")
    #     if(color_size):
    #         for item in color_size:
    #             value = item.tenvalue.split("-")
    #             if value[0] not in colors:
    #                 colors.append(value[0])
    #             if value[1] not in sizes:
    #                 sizes.append(value[1])
    #     else:
    #             for item in colorAttribute:
    #                 colors.append(item.tenvalue)
    #             for item in sizeAttribute:
    #                 sizes.append(item.tenvalue)
    #     context.update({'color_size':list(color_size.values()),'colorAttribute':list(colorAttribute.values()),'sizeAttribute':list(sizeAttribute.values()), 'colors':colors, 'sizes':sizes })
    #-----------------------------------------------------------------------------------------------------------------------------
    
    variants = ProductVariant.objects.filter(product_id=id)
    productAttributes = ProductAttribute.objects.filter(product_id = id)
    variantValues = VariantValue.objects.filter(product_id__product_id = id)
    colors = []
    sizes = []
    if productAttributes != None:
        for attribute in productAttributes:
            attributeValues =  VariantValue.objects.filter(product_id__product_id = id, attribute_id = attribute)
            if attribute.attribute_id.tenthuoctinh == "color":
                for itemvalue in attributeValues:
                    if itemvalue.value not in colors:
                        colors.append(itemvalue.value)
            else:
               for itemvalue in attributeValues:
                    if itemvalue.value not in sizes:
                        sizes.append(itemvalue.value)      

    context.update({'variantValues': list(variantValues.values()), 'productAttributes': list(productAttributes.values()), 'colors': colors, 'sizes': sizes, 'variants': list(variants.values())})



 


    if request.method == 'GET' and request.is_ajax() == False :
        return render(request,'product_detail.html',context)
    elif request.GET.get('type') == "rv":
        page = request.GET.get('page')
        reviews = paginator.page(int(page))
        review_li = list(reviews.object_list.values('user_profile__first_name','user_profile__last_name','subject','noidung','rating','createdat'))
        result = {'review_li': review_li}
        return JsonResponse(result)
    elif request.GET.get('type') == "cm":
        page = request.GET.get('page')
        comments = commentPaginator.page(int(page))
        comment_li = list(comments.object_list.values('id','user_profile__hovaten','noidung','createdat','user_profile__image'))
        commentReplys = []
        for comment in comments:
            replys = Productcommentreply.objects.filter( productcommentid = comment).values('productcommentid_id','user_profile__hovaten','noidung','createdat','user_profile__image')
            commentReplys.extend(list(replys))
        result = {'comment_li': comment_li,
                    'comment_rep': commentReplys}
        return JsonResponse(result)

def addreview(request,id):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid() :
            data = Review()
            data.subject = form.cleaned_data['subject']
            data.noidung = form.cleaned_data['noidung']
            data.rating = form.cleaned_data['rating']
            data.productid_id = id
            data.taikhoanid_id = request.user.id
            data.createdat = date.today()
            data.save()
            messages.success(request, "Đánh giá của bạn đã được ghi nhận")
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)

def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() :
            data = Productcomment()
            data.noidung = form.cleaned_data['noidung']
            data.productid_id = id
            data.user_profile= UserProfile.objects.get(user_id = request.user.id)
            data.createdat = date.today()
            data.save()
            messages.success(request, "Bình luận thành công")
            return HttpResponseRedirect(url)

def addcommentreply(request,id):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() :
            data = Productcommentreply()
            data.noidung = form.cleaned_data['noidung']
            data.productcommentid_id = id
            data.user_profile = UserProfile.objects.get(user_id = request.user.id)
            data.createdat = date.today()
            data.save()
            messages.success(request, "Bình luận thành công")
            return HttpResponseRedirect(url)


def category_products(request, type, theloai):
    try:
        if type == 'book':
            products = Product.objects.raw(
                'SELECT * '
                'FROM product as p '
                'LEFT JOIN sachtype s on p.id = s.ProductID '
                'WHERE s.TheLoaiSachID = %s', [theloai])
        elif type == 'electro':
            products = Product.objects.raw(
                'SELECT * '
                'FROM product as p '
                'LEFT JOIN dientutype d on p.id = d.ProductID '
                'WHERE d.ChiTietTheLoaiDienTuID = %s', [theloai])
        elif type == 'aoquan':
            products = Product.objects.raw(
                'SELECT * '
                'FROM product as p '
                'LEFT JOIN aoquan a on p.id = a.ProductID '
                'WHERE a.TheLoaiQuanAoID = %s', [theloai])
        else:
            products = None
    except:
        pass
    # try:
    #     products = Product.objects.raw(
    #         'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
    #         'FROM product_product as p '
    #         'LEFT JOIN product_productlang as l '
    #         'ON p.id = l.product_id '
    #         'WHERE p.category_id=%s and l.lang=%s', [id])
    # except:
    #     pass

    context={'products': products,
            'productType': type }

    return render(request,'category_products.html',context)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            type = form.cleaned_data['type']
            if type=='0':
                products = Product.objects.filter(ten__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(ten__icontains=query,type=type)
            # category = Category.objects.all()
            context = {'products': products, 'query':query }
                      #  'category': category }
            
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')




# ORDER
#------------------------------------------------------------------------------------------
@login_required(login_url='/login') # Check login
def addtoshopcart(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            variantid = form.cleaned_data['variant_id']
            checkinvariant = Cart.objects.filter(variant_id=variantid, taikhoanid__id=current_user.id)  # Check product in shopcart
            if checkinvariant:
                control = 1 # The product is in the cart
            else:
                control = 0 # The product is not in the cart"""


            if control==1: # Update  shopcart
                data = Cart.objects.get(variant_id=variantid, taikhoanid__id=current_user.id)
                data.soluong += form.cleaned_data['soluong']
                data.save()  # save data
            else : # Inser to Shopcart
                data = Cart()
                data.taikhoanid = current_user
                data.variant_id = variantid
                data.soluong = form.cleaned_data['soluong']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    # else: # if there is no post
    #     if control == 1:  # Update  shopcart
    #         data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
    #         data.quantity += 1
    #         data.save()  #
    #     else:  #  Inser to Shopcart
    #         data = ShopCart()  # model ile bağlantı kur
    #         data.user_id = current_user.id
    #         data.product_id = id
    #         data.quantity = 1
    #         data.variant_id =None
    #         data.save()  #
    #     messages.success(request, "Product added to Shopcart")
    #     return HttpResponseRedirect(url)


def shopcart(request):
    current_user = request.user  # Access User Session information
    cart = Cart.objects.filter(taikhoanid__id=current_user.id)
    cartTotal=0
    for rs in cart:
        cartTotal += rs.total
    context={'cart': cart,
             'total': cartTotal}
    return render(request,'cart.html',context)

@login_required(login_url='/login') # Check login
def deletefromcart(request,id):
    Cart.objects.filter(variant_id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    current_user = request.user
    cart = Cart.objects.filter(taikhoanid=current_user)
    cartTotal = 0
    for rs in cart:
        cartTotal += rs.total

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            shipment = Shipment()
            shipment.donvivanchuyenid = Donvivanchuyen.objects.get(id = int(form.cleaned_data['dvvc']))
            shipment.giaship = 0
            shipment.address = form.cleaned_data['name']+","+form.cleaned_data['address'] + "," +form.cleaned_data['city']+","+form.cleaned_data['phone']
            shipment.save()

            payment = Payment()
            payment.paymentmethodid = Paymentmethod.objects.get(id=1)
            payment.save()


            order = Order()
            order.taikhoanid = current_user
            order.tongtien = cartTotal
            order.status = "WAITING"
            order.createat = date.today()
            order.shipmentid = shipment
            order.paymentid = payment
            order.save()

            for rs in cart:
                detail = Orderdetail()
                detail.orderid     = order
                detail.variantid   = rs.variant_id
                detail.productid = rs.variant_id.product_id
                detail.soluong     = rs.soluong
                detail.gia = rs.total
                detail.save()

                variant = ProductVariant.objects.get(variant_id=rs.variant_id.variant_id)
                variant.quantity -= rs.soluong
                variant.save()

            Cart.objects.filter(taikhoanid = current_user).delete() # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/orderproduct")

    form= OrderForm()
    profile = UserProfile.objects.get(user = current_user)
    context = {'cart': cart,
               'total': cartTotal,
               'form': form,
               'profile': profile,
               }
    return render(request, 'order_form.html', context)


def browserInvoice(request):
    status = request.GET.get('status','')
    if status == 'WAITING':
        allOrder = Order.objects.filter(status = 'WAITING'); # get All Order
    else:
        allOrder = Order.objects.all(); # get All Order
    
    list = []
    for order in allOrder:
        browserOrderForm = BrowserOrderForm()
        browserOrderForm.maDonHang = str(order.id)
        browserOrderForm.ngayDat = str(order.createdat)
        browserOrderForm.khachHang = UserProfile.objects.get(user = order.taikhoanid).hovaten
        payment = Payment.objects.get(id = order.id)
        paymentMethod = Paymentmethod.objects.get(id = payment.paymentmethodid.id).tenpthuc
        if paymentMethod == "cash":
            thanhToan = "Thanh toán bằng tiền mặt"
        elif paymentMethod == "AirPay":
            thanhToan = "Thanh toán qua ví Airpay"
        else:
            thanhToan = "Thanh toán qua ví Momo"

        if order.status == "WAITING":
            tinhTrang = "Chưa xuất"
        elif order.status == "DELIVERING":
            tinhTrang = "Đang vận chuyển"
        else:
            tinhTrang = "NA"

        tongTien = str(order.tongtien) + " VND"
        browserOrderForm.thanhToan = thanhToan
        browserOrderForm.tinhTrang = tinhTrang
        browserOrderForm.tongTien = tongTien
        list.append(browserOrderForm)
        
    title = "Duyệt đơn"
    context = {'title':title, 'listOrder':list}
    return render(request, 'browserInvoice.html', context)


def waitingInvoiceDetail(request, orderID):
    order = Order.objects.get(id = orderID) # get order by id
    maDonHang = order.id # ma don hang
    tongTien = order.tongtien # tong tien
    nguoiDatHang = UserProfile.objects.get(user = order.taikhoanid).hovaten # Ho va ten nguoi dat hang
    thoiGianDatHang = order.createdat # thoi gian dat hang

    # lay toan bo thong tin giao hang cua user
    user = UserProfile.objects.get(user = order.taikhoanid).user
    thongTinGiaoHang = Thongtingiaohang.objects.filter(khachhangid = user)
    # lay toan bo thong tin giao hang cua user

    #dia chi nhan hang
    diaChiNhanHang = ''
    for item in thongTinGiaoHang:
        if str(ord(item.macdinh)) == '1': # neu dia chi nhan hang la mac dinh (isDefault == True)
            diaChiNhanHang = item.diachi
    #end dia chi nhan hang        
    
    #phuong thuc thanh toan
    payment = Payment.objects.get(id = order.id)
    paymentMethod = Paymentmethod.objects.get(id = payment.paymentmethodid.id).tenpthuc
    if paymentMethod == "cash":
        phuongThucThanhToan = "Thanh toán bằng tiền mặt"
    elif paymentMethod == "AirPay":
        phuongThucThanhToan = "Thanh toán qua ví Airpay"
    else:
        phuongThucThanhToan = "Thanh toán qua ví Momo"
    #end phuong thuc thanh toan

    orderDetail = Orderdetail.objects.filter(orderid = order)
    #STT	Mã mặt hàng	Thông tin mặt hàng	Phân loại hàng	Đơn giá	Số lượng	Thành tiền
    listOrderDetail = []
    stt = 1
    for item in orderDetail:
        orderDetailForm = OrderDetailForm()
        orderDetailForm.stt = str(stt)
        orderDetailForm.maMatHang = str(item.productid.id)
        orderDetailForm.thongTinMatHang = item.productid.ten
        orderDetailForm.phanLoaiHang = item.variantid.variant_name
        orderDetailForm.donGia = str(item.gia) + ' VND'
        orderDetailForm.soLuong = str(item.soluong)
        orderDetailForm.thanhTien = str(item.gia*item.soluong) + ' VND'
        listOrderDetail.append(orderDetailForm)
        stt = stt+1
    title = "Chi tiết đơn hàng chưa xuất"
    context = {'title':title, 
    'maDonHang':maDonHang, 'tongTien':tongTien, 
    'nguoiDatHang':nguoiDatHang, 'thoiGianDatHang':thoiGianDatHang,
    'diaChiNhanHang':diaChiNhanHang,'phuongThucThanhToan':phuongThucThanhToan, 'listOrderDetail':listOrderDetail}
    return render(request, 'waitingInvoiceDetail.html', context)


def exportInvoice(request):
    if request.method == 'POST':
        form = ExportInvoiceForm(request.POST)
        if form.is_valid():
            maDonHang = form.cleaned_data['orderId']
            status = form.cleaned_data['status']
            order = Order.objects.get(id = maDonHang)
            if status == 'WAITING':
                order.status = 'WAITING'
            else:
                order.status = 'DELIVERING'
            current_user = request.user
            order.nhanvienxuatid = current_user
            order.updateat = datetime.now()
            order.save()
        return HttpResponseRedirect('/browserInvoice')

    