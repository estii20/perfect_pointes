from django import forms
from .models import PointeShoeProduct, Category, PointeShoe, Width, Size, Color


class ProductForm(forms.ModelForm):
    class Meta:
        model = PointeShoeProduct
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class PointeShoeForm(forms.ModelForm):
    class Meta:
        model = PointeShoe
        fields = '__all__'


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        friendly_names = [(size.id, size.get_friendly_name()) for size in Size.objects.all()]
        self.fields['size'].choices = friendly_names


class WidthForm(forms.ModelForm):
    class Meta:
        model = Width
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        friendly_names = [(width.id, width.get_friendly_name()) for width in Width.objects.all()]
        self.fields['width'].choices = friendly_names


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        friendly_names = [(color.get_friendly_name(), color.get_friendly_name()) for color in Color.objects.all()]
        self.fields['name'].widget = forms.Select(choices=friendly_names)
