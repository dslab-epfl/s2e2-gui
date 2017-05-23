from django.db import models

class Analysis(models.Model):
    s2e_num = models.IntegerField()
    binary_checksum = models.CharField(max_length=256)
    binary_name = models.CharField(max_length=256)
    
    def __str__(self):
        return str(self.s2e_num) + ", " + str(self.binary_checksum) + ", " + str(self.binary_name)