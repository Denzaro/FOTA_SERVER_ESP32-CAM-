from django.db import models

# Create your models here.
class ALM_Server(models.Model):
    name = models.TextField(primary_key=True)
    host = models.TextField(default="")

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "ALM Server"
        verbose_name_plural = "ALM Servers"
