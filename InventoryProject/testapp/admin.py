from django.contrib import admin
from testapp.models import item_mstr,brand_mstr,unit_mstr,tbl_purchase_mstr,tbl_purchase_details,tbl_sales_master,table_sales_details,sales_report,purchase_report
# Register your models here.

class Admin_item_mstr(admin.ModelAdmin):
    list_display = ["name","brand_id","unit_id","item_code","rate","status","username","datetime"]
admin.site.register(item_mstr,Admin_item_mstr)

class Admin_unit_mstr(admin.ModelAdmin):
    list_display = ["unit","unit_code","status","username","datetime"]
admin.site.register(unit_mstr,Admin_unit_mstr)

class Admin_brand_mstr(admin.ModelAdmin):
    list_display = ["name","status","username","datetime"]
admin.site.register(brand_mstr,Admin_brand_mstr)

class Admin_tbl_purchase_mstr(admin.ModelAdmin):
    list_display = ["invoice_no","invoice_date","total_amount","name","contact_no",
                    "status","username","datetime","gst"]
admin.site.register(tbl_purchase_mstr,Admin_tbl_purchase_mstr)

class Admin_tbl_purchase_details(admin.ModelAdmin):
    list_display = ["purcahse_mstr_id","item_id","quantity","gst",
                    "amount","rate","status","username","datetime"]
admin.site.register(tbl_purchase_details,Admin_tbl_purchase_details)

class Admin_tbl_sales_master(admin.ModelAdmin):
    list_display = ["invoice_no","invoice_date","total_amount","name","contact_no",
                    "status","username","datetime","gst"]
admin.site.register(tbl_sales_master,Admin_tbl_sales_master)

class Admin_table_sales_master(admin.ModelAdmin):
    list_display = ["sales_mstr_id","item_id","quantity","gst",
                    "amount","rate","status","username","datetime"]
admin.site.register(table_sales_details,Admin_table_sales_master)

class Admin_sales_report(admin.ModelAdmin):
    list_display = ["item","search_date"]
admin.site.register(sales_report,Admin_sales_report)

class Admin_purchase_report(admin.ModelAdmin):
    list_display = ["item", "search_date"]
admin.site.register(purchase_report,Admin_purchase_report)