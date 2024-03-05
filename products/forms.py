from django import forms
from django.core.exceptions import ValidationError 
from .widgets import CustomClearableFileInput
from .models import (
    PointeShoe, Size, Width, Color,
    PointeShoeBrand, PointeShoeProduct
)


class PointeShoeProductForm(forms.ModelForm):
    new_pointe_shoe_name = forms.CharField(
        label='Pointe Shoe Name', max_length=100, required=False)
    new_pointe_shoe_sku = forms.CharField(
        label='SKU', max_length=50, required=False)
    new_pointe_shoe_shank = forms.ChoiceField(
        choices=PointeShoe.shank_choices, required=False)
    new_pointe_shoe_color = forms.ModelChoiceField(
        queryset=Color.objects.all(), 
        empty_label=None, label='Color', required=False)
    new_pointe_shoe_price = forms.DecimalField(
        label='Price', 
        max_digits=10, decimal_places=2, required=False)
    new_pointe_shoe_arch = forms.ChoiceField(
        choices=PointeShoe.arch_choices, 
        label='Arch', required=False)
    new_pointe_shoe_ribbon = forms.ChoiceField(
        choices=PointeShoe.ribbon_choices, 
        label='Ribbon', required=False)
    image = forms.ImageField(
        label='Image', required=False, 
        widget=CustomClearableFileInput)
    brand = forms.ModelChoiceField(
        queryset=PointeShoeBrand.objects.all(), 
        label='Brand', required=True)
    available_sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(), required=False, 
        widget=forms.CheckboxSelectMultiple, 
        label='Available Sizes')
    available_widths = forms.ModelMultipleChoiceField(
        queryset=Width.objects.all(), required=False, 
        widget=forms.CheckboxSelectMultiple, 
        label='Available Widths')
    status = forms.ChoiceField(
        choices=PointeShoe.status_choices, 
        label='Status', required=True)
    feature = forms.CharField(
        label='Feature', 
        widget=forms.Textarea(attrs={'rows': 4}), 
        required=False)

    class Meta:
        model = PointeShoeProduct
        fields = ['title', 'sku', 'image', 'image_url',
                  'price', 'category', 'brand', 'status', 'feature']
        widgets = {
            'sku': forms.HiddenInput(),
            'image': forms.HiddenInput(),
            'image_url': forms.HiddenInput(),
            'price': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['available_sizes'].queryset = Size.objects.all().order_by('size')

    def clean_new_pointe_shoe_sku(self):
        sku = self.cleaned_data['new_pointe_shoe_sku']
        if PointeShoe.objects.filter(sku=sku).exists():
            raise ValidationError("SKU already exists. Please use a different SKU.")
        return sku

    def save(self, commit=True):
        instance = super().save(commit=False)

        new_pointe_shoe_sku = self.cleaned_data.get('new_pointe_shoe_sku')
        if new_pointe_shoe_sku:
            if PointeShoe.objects.filter(sku=new_pointe_shoe_sku).exists():
                raise ValidationError("SKU already exists. Please use a different SKU.")

        pointe_shoe, created = PointeShoe.objects.get_or_create(
            sku=self.cleaned_data['new_pointe_shoe_sku'],
            defaults={
                'name': self.cleaned_data['new_pointe_shoe_name'],
                'shank': self.cleaned_data['new_pointe_shoe_shank'],
                'color': self.cleaned_data['new_pointe_shoe_color'],
                'price': self.cleaned_data['new_pointe_shoe_price'],
                'arch': self.cleaned_data['new_pointe_shoe_arch'],
                'ribbon': self.cleaned_data['new_pointe_shoe_ribbon'],
                'brand': self.cleaned_data['brand'],
                'category': instance.category,
                'status': self.cleaned_data['status'],
                'feature': self.cleaned_data['feature'],
            }
        )

        instance.title = pointe_shoe.name
        instance.sku = pointe_shoe.sku
        instance.price = pointe_shoe.price
        instance.pointe_shoe = pointe_shoe

        if commit:
            instance.save()
            instance.pointe_shoe.available_sizes.set(
                self.cleaned_data['available_sizes'])
            instance.pointe_shoe.available_widths.set(
                self.cleaned_data['available_widths'])
            self.save_m2m()
        return instance


class PointeShoeProductEditForm(forms.ModelForm):
    shank = forms.ChoiceField(
        choices=PointeShoe.shank_choices, required=False)
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(), label='Color', 
        required=False, empty_label=None)
    ribbon = forms.ChoiceField(
        choices=PointeShoe.ribbon_choices, 
        label='Ribbon', required=False)
    status = forms.ChoiceField(
        choices=PointeShoe.status_choices, 
        label='Status', required=True)
    feature = forms.CharField(
        label='Feature', 
        widget=forms.Textarea(attrs={'rows': 4}), required=False)
    logo = forms.ImageField(
        label='Logo', required=False, 
        widget=CustomClearableFileInput)
    image = forms.ImageField(
        label='Image', required=False, 
        widget=CustomClearableFileInput)
    brand = forms.ModelChoiceField(
        queryset=PointeShoeBrand.objects.all(), 
        label='Brand', required=True)
    available_sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(), required=False, 
        widget=forms.CheckboxSelectMultiple, label='Available Sizes')
    available_widths = forms.ModelMultipleChoiceField(
        queryset=Width.objects.all(), required=False, 
        widget=forms.CheckboxSelectMultiple, label='Available Widths')

    arch_choices = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    arch = forms.ChoiceField(choices=arch_choices, required=False)

    brand_description = forms.CharField(
        label='Brand Description',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )

    class Meta:
        model = PointeShoeProduct
        fields = ['title', 'image', 'image_url',
                  'price', 'category', 'brand', 'status', 'feature']
        widgets = {
            'sku': forms.HiddenInput(),
            'image': forms.HiddenInput(),
            'image_url': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['available_sizes'].queryset = Size.objects.all().order_by('size')
        instance = kwargs.get('instance')
        if instance:
            brand = instance.pointe_shoe.brand
            self.fields['logo'].initial = brand.logo
            self.fields['feature'].initial = instance.pointe_shoe.feature
            self.fields['shank'].initial = instance.pointe_shoe.shank
            self.fields['color'].initial = instance.pointe_shoe.color
            self.fields['ribbon'].initial = instance.pointe_shoe.ribbon
            self.fields['status'].initial = instance.pointe_shoe.status
            self.fields['arch'].initial = instance.pointe_shoe.arch
            self.fields['category'].initial = instance.pointe_shoe.category
            self.fields['brand_description'].initial = brand.description

            self.initial_brand_description = brand.description
            self.fields['brand_description'] = forms.CharField(
                label='Brand Description',
                widget=forms.Textarea(attrs={'rows': 4}),
                initial=self.initial_brand_description,
                required=False
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            brand = instance.pointe_shoe.brand
            brand.logo = self.cleaned_data['logo']
            
            if hasattr(instance, 'pointe_shoe') and instance.pointe_shoe:
                instance.pointe_shoe.feature = self.cleaned_data['feature']
                instance.pointe_shoe.price = self.cleaned_data['price']
                instance.pointe_shoe.shank = self.cleaned_data['shank']
                instance.pointe_shoe.color = self.cleaned_data['color']
                instance.pointe_shoe.ribbon = self.cleaned_data['ribbon']
                instance.pointe_shoe.status = self.cleaned_data['status']
                instance.pointe_shoe.category = self.cleaned_data['category']
                instance.pointe_shoe.arch = self.cleaned_data['arch']
                instance.pointe_shoe.available_sizes.set(self.cleaned_data['available_sizes'])
                instance.pointe_shoe.available_widths.set(self.cleaned_data['available_widths'])
                instance.pointe_shoe.brand.description = self.cleaned_data['brand_description']
                instance.pointe_shoe.save()

            brand.description = self.cleaned_data['brand_description']
            brand.save()
        return instance
