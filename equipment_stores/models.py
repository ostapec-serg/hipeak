from django.db import models
from django.urls import reverse_lazy
from pytils.translit import slugify
from phonenumber_field.modelfields import PhoneNumberField


class EquipmentStores(models.Model):
    SERVICE_CHOICE = (
        ('sale', 'Sale'),
        ('rent', 'Rent'),
        ('sale|Rent', 'Sale|Rent'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=100, verbose_name="Назва")
    slug = models.SlugField(unique=True, max_length=150)
    description = models.TextField(verbose_name="Опис")
    pub_date = models.DateField(auto_now=True)
    url = models.URLField(null=True)
    phone = PhoneNumberField(blank=True, help_text='Contact phone number',
                             verbose_name="Номер телефону")
    email = models.EmailField(blank=True, null=True)
    store_address = models.CharField(max_length=150, verbose_name="Адресв")
    is_active = models.BooleanField(default=False)
    location = models.CharField(max_length=500, blank=True)
    service = models.CharField(choices=SERVICE_CHOICE, null=True, max_length=11)
    img = models.ImageField(null=True, upload_to='stores_images/',
                            blank='true', verbose_name='stores_images/')

    def save(self, *args, **kwargs):
        """Auto save slug"""
        self.slug = slugify(self.name)
        super(EquipmentStores, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.service}"

    def get_absolute_url(self):
        """Return absolute url """
        return reverse_lazy("equipment_stores:detail", kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазини'
