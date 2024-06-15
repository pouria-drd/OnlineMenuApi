import uuid
from PIL import Image
from django.db import models
from django_cleanup import cleanup
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from menus.models import Menu


def category_icon_upload_to(instance, filename):
    """Generate a unique upload path for category icons."""
    return f"{instance.menu.slug}/category_icons/{instance.id}/{filename}"


@cleanup.select
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.RESTRICT, related_name="categories")

    name = models.CharField(_("name"), max_length=60)
    icon = models.ImageField(_("icon"), upload_to=category_icon_upload_to, blank=True)

    is_active = models.BooleanField(_("is active"), default=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["menu", "is_active"]),
        ]

    def __str__(self):
        return self.name + " " + f"({self.menu.name})"

    def clean(self):
        super().clean()

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


@receiver(models.signals.post_save, sender=Category)
def resize_icon(sender, instance, **kwargs):
    """Resize the icon image if it's larger than 512x512 pixels."""
    if instance.icon:
        img = Image.open(instance.icon.path)
        if img.width > 512 or img.height > 512:
            img.thumbnail((512, 512))
            img.save(instance.icon.path)
