from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
from random import randint
def generate_item_code():
    return randint(1001, 9999)

def generate_unit_code():
    return randint(1001, 9999)

#--------Unit------------------
class unit_mstr(models.Model):
    Kg = 'Kg'
    Litre = 'Liter'
    Piece = 'Piece'

    UNIT_CHOICES = [
        (Kg, 'Kg'),
        (Litre, 'Liter'),
        (Piece, 'Piece'),
    ]

    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    unit_code = models.IntegerField(default=generate_unit_code)
    status=models.BooleanField(default=True)
    username=models.CharField(max_length=25)
    datetime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.unit

#-------------Brand-----------------

class brand_mstr(models.Model):
    name=models.CharField(max_length=30)
    status=models.BooleanField(default=True)
    username=models.CharField(max_length=25)
    datetime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#-----------Item-------------

class item_mstr(models.Model):
    name=models.CharField(max_length=25)
    brand_id=models.ForeignKey(brand_mstr,on_delete=models.CASCADE)
    unit_id=models.ForeignKey(unit_mstr,on_delete=models.CASCADE)
    item_code=models.IntegerField(default=generate_item_code)
    rate = models.FloatField()
    stock = models.IntegerField(default=0)  # purchase pe badhta hai, sale pe ghatta hai
    #quantity=models.IntegerField()
    #total=models.FloatField()
    status=models.BooleanField(default=True)
    username=models.CharField(max_length=25)
    datetime=models.DateTimeField(auto_now_add=True)

    """def save(self,*args,**kwargs):
        self.total=self.quantity * self.rate
        super(item_mstr,self).save()"""
    def __str__(self):
        return self.name


#-------------Purchase-----------------

GST_CHOICES = [
    (12, '12%'),
    (15, '15%'),
    (18, '18%'),
]

def generate_invoice_no():
    return randint(1001, 9999)

# PhoneNumber
phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)

class tbl_purchase_mstr(models.Model):
    invoice_no=models.IntegerField(default=generate_invoice_no)
    invoice_date=models.DateTimeField(auto_now_add=False)
    total_amount=models.FloatField(default=0)
    name=models.CharField(max_length=25)
    contact_no=models.CharField(max_length=10, validators=[phone_validator])
    status=models.BooleanField(default=True)
    username=models.CharField(max_length=30)
    datetime=models.DateTimeField(auto_now_add=True)
    gst=models.FloatField(default=18, choices=GST_CHOICES)
    igst=models.FloatField(default=0)
    cgst=models.FloatField(default=0)
    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.igst = self.gst / 2
        self.cgst = self.gst / 2
        super(tbl_purchase_mstr,self).save(*args,**kwargs)

class tbl_purchase_details(models.Model):
    purcahse_mstr_id=models.ForeignKey(tbl_purchase_mstr,on_delete=models.CASCADE)
    item_id=models.ForeignKey(item_mstr,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    gst = models.FloatField(default=18, choices=GST_CHOICES)
    igst=models.FloatField(default=0)
    cgst=models.FloatField(default=0)
    amount=models.FloatField()
    rate=models.FloatField()
    status=models.BooleanField(default=True)
    username=models.CharField(max_length=30)
    datetime=models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        base_amount = (self.rate * self.quantity)
        gst_amount = (base_amount * self.gst / 100)
        self.amount = (base_amount + gst_amount)
        self.igst = self.gst / 2
        self.cgst = self.gst / 2
        super(tbl_purchase_details,self).save(*args,**kwargs)


#---------------------Sales------------------

class tbl_sales_master(models.Model):
    invoice_no=models.IntegerField(default=generate_invoice_no)
    invoice_date=models.DateTimeField(auto_now_add=False)
    total_amount=models.FloatField(default=0)
    name=models.CharField(max_length=25)
    contact_no=models.CharField(max_length=10, validators=[phone_validator])
    status=models.BooleanField(default=True)
    username=models.CharField(max_length=30)
    datetime=models.DateTimeField(auto_now_add=True)
    gst = models.FloatField(default=18, choices=GST_CHOICES)
    igst=models.FloatField(default=0)
    cgst=models.FloatField(default=0)
    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.igst = self.gst / 2
        self.cgst = self.gst / 2
        super(tbl_sales_master,self).save(*args,**kwargs)

class table_sales_details(models.Model):
    sales_mstr_id=models.ForeignKey(tbl_sales_master,on_delete=models.CASCADE)
    item_id=models.ForeignKey(item_mstr,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    gst = models.FloatField(default=18, choices=GST_CHOICES)
    igst=models.FloatField(default=0)
    cgst=models.FloatField(default=0)
    amount=models.FloatField()
    rate=models.FloatField()
    status=models.BooleanField(default=True)
    username=models.CharField(max_length=30)
    datetime=models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        base_amount = (self.rate * self.quantity)
        gst_amount = (base_amount * self.gst / 100)
        self.amount = (base_amount + gst_amount)
        self.igst = self.gst / 2
        self.cgst = self.gst / 2
        super(table_sales_details,self).save(*args,**kwargs)


# Model for Sales Report
class sales_report(models.Model):
    item = models.ForeignKey(item_mstr, on_delete=models.CASCADE)
    search_date = models.DateField(null=True, blank=True)


# Model for Purchase Report
class purchase_report(models.Model):
    item = models.ForeignKey(item_mstr, on_delete=models.CASCADE)
    search_date = models.DateField(null=True, blank=True)