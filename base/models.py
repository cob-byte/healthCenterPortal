from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class HealthCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class HealthCenterManager(BaseUserManager):
    def create_user(self, email, firstName, middleName, lastName, date_of_birth, health_center, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            middleName=middleName,
            lastName=lastName,
            date_of_birth=date_of_birth,
            health_center=health_center
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, middleName, lastName, date_of_birth, health_center,password=None):
        user = self.create_user(
            email=email,
            firstName=firstName,
            middleName=middleName,
            lastName=lastName,
            date_of_birth=date_of_birth,
            health_center=health_center,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class HealthWorker(AbstractBaseUser, PermissionsMixin):
    HEALTH_CENTER_CHOICES = [
        ('HC1', 'Health Center 1'),
        ('HC2', 'Health Center 2'),
        ('HC3', 'Health Center 3'),
        ('HC4', 'Health Center 4'),
        ('HC5', 'Health Center 5'),
        ('HC6', 'Health Center 6'),
    ]

    health_center = models.CharField(max_length=3, choices=HEALTH_CENTER_CHOICES)

    email = models.EmailField(unique=True, max_length=255, default='example@gmail.com')

    firstName = models.CharField(max_length=100, verbose_name='First Name')
    middleName = models.CharField(max_length=100, blank=True, default="", verbose_name='Middle Name')
    lastName = models.CharField(max_length=100, verbose_name='Last Name')
    date_of_birth = models.DateField()

    is_healthworker = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    objects = HealthCenterManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'middleName', 'lastName', 'date_of_birth', 'health_center']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Patient(models.Model):
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_of_visit = models.DateField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, validators=[MaxValueValidator(60.0), MinValueValidator(20.0)])
    blood_pressure_systolic = models.PositiveSmallIntegerField(validators=[MaxValueValidator(300)])
    blood_pressure_diastolic = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200)])
    pulse_rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(300)])
    respiratory_rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    symptoms = models.TextField()
    diagnosis = models.TextField()
    prescribed_medicines = models.TextField()
    notes = models.TextField()

    def __str__(self):
        return f'{self.patient} - {self.date_of_visit}'

class MedicalSupply(models.Model):
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    prescription_date = models.DateField()
    instructions = models.CharField(max_length=255)
    details = models.TextField()
    dosage = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.medicine_name} - {self.dosage}'

class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.patient} - {self.date}'

class OutbreakReport(models.Model):
    DISEASE_CHOICES = [
        ('Dengue', 'Dengue'),
        ('Measles', 'Measles'),
        ('Leptospirosis', 'Leptospirosis'),
    ]

    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]

    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2016), MaxValueValidator(datetime.datetime.now().year)])
    month = models.CharField(max_length=9, choices=MONTH_CHOICES)
    disease = models.CharField(max_length=20, choices=DISEASE_CHOICES)
    cases = models.IntegerField()
    deaths = models.IntegerField()

    def __str__(self):
        return f'{self.disease} Report - {self.health_center} - {self.month}, {self.year}'

class Appointment(models.Model):
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    health_worker = models.ForeignKey(HealthWorker, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')

    class Meta:
        unique_together = ('health_center', 'date')

    def __str__(self):
        return f"{self.patient} - {self.health_center} - {self.date}"