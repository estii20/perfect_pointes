from django import forms
from .widgets import CustomClearableFileInput
from .models import PointeShoe, Size, Width, Color, PointeShoeBrand, PointeShoeProduct


class PointeShoeProductForm(forms.ModelForm):
    new_pointe_shoe_name = forms.CharField(label='Pointe Shoe Name', max_length=100, required=False)
    new_pointe_shoe_sku = forms.CharField(label='SKU', max_length=50, required=False)
    new_pointe_shoe_width = forms.ChoiceField(choices=PointeShoe.width_choices, required=False)
    new_pointe_shoe_shank = forms.ChoiceField(choices=PointeShoe.shank_choices, required=False)
    new_pointe_shoe_color = forms.ModelChoiceField(queryset=Color.objects.all(), empty_label=None, label='Color', required=False)
    new_pointe_shoe_price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2, required=False)
    new_pointe_shoe_arch = forms.ChoiceField(choices=PointeShoe.arch_choices, label='Arch', required=False)
    new_pointe_shoe_ribbon = forms.ChoiceField(choices=PointeShoe.ribbon_choices, label='Ribbon', required=False)
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)
    brand = forms.ModelChoiceField(queryset=PointeShoeBrand.objects.all(), label='Brand', required=True) 
    available_sizes = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label='Available Sizes')
    available_widths = forms.ModelMultipleChoiceField(queryset=Width.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label='Available Widths')
    status = forms.ChoiceField(choices=PointeShoe.status_choices, label='Status', required=True) 
    feature = forms.CharField(label='Feature', widget=forms.Textarea(attrs={'rows': 4}), required=False)


    class Meta:
        model = PointeShoeProduct
        fields = ['title', 'availability', 'sku', 'image', 'image_url', 'price', 'category', 'brand', 'status', 'feature']

        widgets = {
            'sku': forms.HiddenInput(),
            'image': forms.HiddenInput(),
            'image_url': forms.HiddenInput(),
            'price': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['new_pointe_shoe_sku'].initial = instance.pointe_shoe.sku
            self.fields['feature'].initial = instance.pointe_shoe.feature
            self.fields['new_pointe_shoe_price'].initial = instance.pointe_shoe.price

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    def save(self, commit=True):
        pointe_shoe_instance = None  
        if self.cleaned_data['new_pointe_shoe_name'] and self.cleaned_data['new_pointe_shoe_sku']:
            pointe_shoe_instance = PointeShoe.objects.filter(sku=self.cleaned_data['new_pointe_shoe_sku']).first()

            if pointe_shoe_instance:
                pointe_shoe_instance.name = self.cleaned_data['new_pointe_shoe_name']
                pointe_shoe_instance.width = self.cleaned_data['new_pointe_shoe_width']
                pointe_shoe_instance.shank = self.cleaned_data['new_pointe_shoe_shank']
                pointe_shoe_instance.color = self.cleaned_data['new_pointe_shoe_color']
                pointe_shoe_instance.price = self.cleaned_data['new_pointe_shoe_price']
                pointe_shoe_instance.arch = self.cleaned_data['new_pointe_shoe_arch']
                pointe_shoe_instance.ribbon = self.cleaned_data['new_pointe_shoe_ribbon']
                pointe_shoe_instance.brand = self.cleaned_data['brand']
                pointe_shoe_instance.category = self.instance.category
                pointe_shoe_instance.status = self.cleaned_data['status']
                pointe_shoe_instance.feature = self.cleaned_data['feature']
                pointe_shoe_instance.save()
            else:
                pointe_shoe_instance = PointeShoe.objects.create(
                    name=self.cleaned_data['new_pointe_shoe_name'],
                    sku=self.cleaned_data['new_pointe_shoe_sku'],
                    width=self.cleaned_data['new_pointe_shoe_width'],
                    shank=self.cleaned_data['new_pointe_shoe_shank'],
                    color=self.cleaned_data['new_pointe_shoe_color'],
                    price=self.cleaned_data['new_pointe_shoe_price'],
                    arch=self.cleaned_data['new_pointe_shoe_arch'],
                    ribbon=self.cleaned_data['new_pointe_shoe_ribbon'],
                    brand=self.cleaned_data['brand'],
                    category=self.instance.category,
                    status=self.cleaned_data['status'],
                    feature=self.cleaned_data['feature'],
                )
                pointe_shoe_instance.available_sizes.set(self.cleaned_data['available_sizes'])
                pointe_shoe_instance.available_widths.set(self.cleaned_data['available_widths'])

        else:
            pointe_shoe_instance = self.instance.pointe_shoe

            pointe_shoe_instance.name = self.cleaned_data['new_pointe_shoe_name']
            pointe_shoe_instance.width = self.cleaned_data['new_pointe_shoe_width']
            pointe_shoe_instance.shank = self.cleaned_data['new_pointe_shoe_shank']
            pointe_shoe_instance.color = self.cleaned_data['new_pointe_shoe_color']
            pointe_shoe_instance.price = self.cleaned_data['new_pointe_shoe_price']
            pointe_shoe_instance.arch = self.cleaned_data['new_pointe_shoe_arch']
            pointe_shoe_instance.ribbon = self.cleaned_data['new_pointe_shoe_ribbon']
            pointe_shoe_instance.brand = self.cleaned_data['brand']
            pointe_shoe_instance.category = self.instance.category
            pointe_shoe_instance.status = self.cleaned_data['status']
            pointe_shoe_instance.feature = self.cleaned_data['feature']
            pointe_shoe_instance.save()

        self.instance.pointe_shoe = pointe_shoe_instance

        return super().save(commit)

