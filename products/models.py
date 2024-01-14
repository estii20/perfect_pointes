from django.db import models


class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class PointeShoeBrand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class PointeShoe(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    size = models.CharField(max_length=50)
    brand = models.ForeignKey(PointeShoeBrand, on_delete=models.CASCADE)
    width_choices = [
        ('x', 'X'),
        ('xx', 'XX'),
        ('xxx', 'XXX'),
        ('xxxx', 'XXXX'),
        ('xxxxx', 'XXXXX'),
    ]
    width = models.CharField(max_length=5, choices=width_choices)
    shank_choices = [
        ('ss', 'SS'),
        ('s', 'S'),
        ('m', 'M'),
        ('h', 'H'),
        ('sh', 'SH'),
    ]
    shank = models.CharField(max_length=2, choices=shank_choices)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('beginner', 'Beginner'),
        ('advanced', 'Advanced'),
    ]
    status = models.CharField(max_length=50, choices=status_choices)
    arch_choices = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    arch = models.CharField(max_length=10, choices=arch_choices)
    link = models.URLField(max_length=200, blank=True, null=True)
    ribbon_choices = [
        ('beige', 'Ribbon Beige'),
        ('pink', 'Ribbon Pink'),
    ]
    ribbon = models.CharField(max_length=5, choices=ribbon_choices)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class PointeShoeProduct(models.Model):
    title = models.CharField(max_length=100)
    pointe_shoe = models.ForeignKey(PointeShoe, on_delete=models.CASCADE)
    brand = models.ForeignKey(PointeShoeBrand, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    sku = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.pointe_shoe.width} - {self.pointe_shoe.shank} - {self.pointe_shoe.ribbon} - {self.pointe_shoe.color} - {self.pointe_shoe.category.name} - {self.pointe_shoe.size} - {self.brand.name}"
