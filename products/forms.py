from django import forms
from .widgets import CustomClearableFileInput
from .models import PointeShoe, Size, Width, Color, Category, PointeShoeBrand, PointeShoeProduct


from django import forms
from .models import PointeShoeProduct, PointeShoe, PointeShoeBrand, Size, Width, Color


class PointeShoeProductForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=PointeShoeBrand.objects.all())
    pointe_shoe = forms.ModelChoiceField(queryset=PointeShoe.objects.all())

    class Meta:
        model = PointeShoeProduct
        fields = '__all__'
        exclude = ['link', 'sku', 'title', 'pointe_shoe', 'image_url']  

    available_sizes = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    available_widths = forms.ModelMultipleChoiceField(queryset=Width.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    shank = forms.ChoiceField(choices=PointeShoe.shank_choices)
    color = forms.ModelChoiceField(queryset=Color.objects.all(), empty_label=None)
    ribbon = forms.ChoiceField(choices=PointeShoe.ribbon_choices)
    arch = forms.ChoiceField(choices=PointeShoe.arch_choices)
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)
    feature = forms.CharField(widget=forms.Textarea)
    new_pointe_shoe_name = forms.CharField(label='Pointe Shoe Name', max_length=100)
    new_pointe_shoe_sku = forms.CharField(label='SKU', max_length=50)
    new_pointe_shoe_price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
            