from django.contrib import admin
from .models import *
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['hovaten', 'gioitinh', 'diachi', 'sodt', 'thethanhvien', 'role', 'image_tag']

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['value', 'hsd', 'requiree']

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user_profile','productid','noidung','createdat']


class ProductCommentReplyAdmin(admin.ModelAdmin):
    list_display = ['productcommentid','user_profile','noidung','createdat']

class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ['productid','discountid']


class ProductAttributeAdmin(admin.ModelAdmin):
	list_display = ['product_id','attribute_id']

class AttributeAdmin(admin.ModelAdmin):
	list_display = ['tenthuoctinh']

class ProductVariantAdmin(admin.ModelAdmin):
	list_display = ['variant_id','product_id','variant_name','price','quantity','image_tag']

class VariantValueAdmin(admin.ModelAdmin):
	list_display = ['product_id','variant_id','attribute_id','value']

class DonViVanChuyenAdmin(admin.ModelAdmin):
    list_display = ['id','tendonvivanchuyen']

class OrdernAdmin(admin.ModelAdmin):
    list_display = ['id','taikhoanid','tongtien','status','createdat', 'updateat','phuongthucthanhtoan','phuongthucvanchuyen', 'nhanvienxuat']

    
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id','orderid','productid','variantid','soluong','gia']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','sothe','tenchuthe','ngayphathanh','ngayhethan','phuongthucthanhtoan']


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id','tenpthuc']


class LoaiDiaChiAdmin(admin.ModelAdmin):
    list_display = ['id','loai']


class ThongtingiaohangAdmin(admin.ModelAdmin):
    list_display = ['id','tenkhachhang', 'hoten','diachi','sodt','isDefault','thanhpho','quan','phuong','loaidiachi']

admin.site.register(Product)
admin.site.register(Tacgia)
admin.site.register(Nhaxuatban)
admin.site.register(Theloaisach)
admin.site.register(Chitiettheloaisach)
admin.site.register(Sachtype)
admin.site.register(Review)
admin.site.register(Thethanhvien)
admin.site.register(Role)
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Hinhanhsanpham)
admin.site.register(Productcomment,ProductCommentAdmin)
admin.site.register(Productcommentreply,ProductCommentReplyAdmin)
admin.site.register(Order,OrdernAdmin)
admin.site.register(Orderdetail,OrderDetailAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Shipment)
admin.site.register(Paymentmethod,PaymentMethodAdmin)
admin.site.register(Donvivanchuyen, DonViVanChuyenAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(ProductDiscount,ProductDiscountAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Attributevalue)

admin.site.register(Theloaidientu)
admin.site.register(Theloaiquanao)


admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductVariant,ProductVariantAdmin)
admin.site.register(VariantValue,VariantValueAdmin)


admin.site.register(Thongtingiaohang,ThongtingiaohangAdmin)
admin.site.register(Loaidiachi,LoaiDiaChiAdmin)
admin.site.register(Thanhpho)
admin.site.register(Quan)
admin.site.register(Phuong)
