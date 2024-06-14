import uuid
from PIL import Image
from django.db import models
from django_cleanup import cleanup
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from categories.models import Category


def category_icon_upload_to(instance, filename):
    """Generate a unique upload path for product icons."""
    return f"product_icons/{instance.category.slug}_{instance.slug}_{instance.id}/{filename}"


@cleanup.select
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="products"
    )

    name = models.CharField(_("name"), max_length=60)
    slug = models.SlugField(_("slug"), max_length=60)
    icon = models.ImageField(_("icon"), upload_to=category_icon_upload_to, blank=True)

    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)

    is_active = models.BooleanField(_("is active"), default=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if (
            Product.objects.filter(category=self.category, slug=self.slug)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                _("The slug must be unique within the same category!")
            )

        if self.icon:
            # Validate the image file type and size
            valid_image_extensions = ["jpg", "jpeg", "png"]
            ext = self.icon.name.split(".")[-1].lower()
            if ext not in valid_image_extensions:
                raise ValidationError(
                    _(
                        "Unsupported file extension. Supported extensions are: jpg, jpeg, png!"
                    )
                )
            if self.icon.size > 1 * 1024 * 1024:  # 1MB limit
                raise ValidationError(_("Image file too large ( > 1MB !"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


@receiver(models.signals.post_save, sender=Category)
def resize_icon(sender, instance, **kwargs):
    """Resize the icon image if it's larger than 512x512 pixels."""
    if instance.icon:
        img = Image.open(instance.icon.path)
        if img.width > 512 or img.height > 512:
            img.thumbnail((512, 512))
            img.save(instance.icon.path)
