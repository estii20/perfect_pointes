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

    def save(self, commit=True):
            instance = super().save(commit=False)
            
            pointe_shoe, created = PointeShoe.objects.get_or_create(
                sku=self.cleaned_data['new_pointe_shoe_sku'],
                defaults={
                    'name': self.cleaned_data['new_pointe_shoe_name'],
                    'width': self.cleaned_data['new_pointe_shoe_width'],
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
                instance.pointe_shoe.available_sizes.set(self.cleaned_data['available_sizes'])
                instance.pointe_shoe.available_widths.set(self.cleaned_data['available_widths'])
                self.save_m2m()
            return instance