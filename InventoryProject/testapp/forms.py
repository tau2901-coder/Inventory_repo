from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from testapp.models import item_mstr,unit_mstr,brand_mstr,tbl_purchase_mstr,tbl_purchase_details,tbl_sales_master,table_sales_details,purchase_report

class item_mstr_form(forms.ModelForm):
    class Meta:
        model=item_mstr
        exclude=['status','username','total','stock']

class unit_mstr_form(forms.ModelForm):
    class Meta:
        model=unit_mstr
        exclude=['status','username']

class brand_mstr_form(forms.ModelForm):
    class Meta:
        model=brand_mstr
        exclude = ['status','username']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username','password1')

class tbl_purchase_mstr_form(forms.ModelForm):
    class Meta:
        model = tbl_purchase_mstr
        exclude = ['status', 'username','total_amount','igst','cgst']
        widgets = {
            'invoice_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

class tbl_purchase_details_form(forms.ModelForm):
    class Meta:
        model=tbl_purchase_details
        exclude = ['status', 'username', 'rate',"amount",'igst','cgst']


class tbl_sales_master_form(forms.ModelForm):
    class Meta:
        model = tbl_sales_master
        exclude = ['status', 'username','total_amount','igst','cgst']
        widgets = {
            'invoice_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

class table_sales_details_form(forms.ModelForm):
    class Meta:
        model=table_sales_details
        exclude = ['status', 'username', 'rate', "amount", 'igst', 'cgst']


class purchase_report_form(forms.Form):
    item = forms.ModelChoiceField(
        queryset=item_mstr.objects.filter(status=True),
        required=False,
        empty_label="All Items",
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date and to_date < from_date:
            self.add_error('to_date', "'To' date cannot be earlier than 'From' date.")
        return cleaned_data


class sales_report_form(forms.Form):
    item = forms.ModelChoiceField(
        queryset=item_mstr.objects.filter(status=True),
        required=False,
        empty_label="All Items",
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date and to_date < from_date:
            self.add_error('to_date', "'To' date cannot be earlier than 'From' date.")
        return cleaned_data