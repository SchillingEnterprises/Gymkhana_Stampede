from django.db import models


# Create your models here.
class Client(models.Model):
    client_first_name = models.CharField(max_length=250)
    client_last_name = models.CharField(max_length=500)
    client_address = models.TextField()
    client_phone_number = models.IntegerField()


class Staff(models.Model):
    staff_first_name = models.CharField(max_length=250)
    staff_middle_name = models.CharField(max_length=1000)
    staff_last_name = models.CharField(max_length=500)
    staff_address = models.TextField()
    staff_phone_number = models.IntegerField()


class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    appointment_start_time = models.DateTimeField()
    staff_member_assigned_to = models.ManyToOneRel(Staff.staff_first_name, Staff.staff_middle_name,
                                                   Staff.staff_last_name)
