from django.db import models
from phone_field import PhoneField


class EquipmentStores(models.Model):
    SERVICES_CHOICE = (
        ('Sale', 'Sale'),
        ('Rent', 'Rent'),
        ('Sale & rent', 'Sale & rent'),
        ('Other', 'Other'),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    img = models.ImageField(null=True, upload_to='stores_images/',
                            blank='true', verbose_name='stores_images/')
    url = models.URLField(null=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField(null=True)
    store_address = models.CharField(max_length=150)
    work_schedule = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)
    services = models.CharField(max_length=11, choices=SERVICES_CHOICE)

    def __str__(self):
        return f"{self.name}: {self.services}"

    def get_absolute_url(self):
        return f"/equipments/store/{self.pk}"

    def __unicode__(self):
        return self.name
