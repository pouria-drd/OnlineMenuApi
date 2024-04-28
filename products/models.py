import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from categories.models import Category

User = get_user_model()


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.RESTRICT
    )
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="prices"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.price}"

    class Meta:
        verbose_name_plural = "Prices"
        ordering = ["-created_at"]
