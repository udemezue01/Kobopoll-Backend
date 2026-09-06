from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    class AccountType(models.TextChoices):
        PERSONAL = 'PERSONAL', 'Personal'
        BUSINESS = 'BUSINESS', 'Business'

    class MaritalStatus(models.TextChoices):
        SINGLE = 'SINGLE', 'Single'
        MARRIED = 'MARRIED', 'Married'
        DIVORCED = 'DIVORCED', 'Divorced'
        WIDOWED = 'WIDOWED', 'Widowed'

    class EducationLevel(models.TextChoices):
        O_LEVEL = 'O_LEVEL', "O'Level (WAEC/NECO)"
        OND_HND = 'OND_HND', 'OND/HND'
        BACHELORS = 'BACHELORS', "Bachelor's Degree"
        POST_GRADUATE = 'POST_GRADUATE', 'Post-Graduate (Master/PhD)'

    class EmploymentStatus(models.TextChoices):
        FORMAL = 'FORMAL', 'Formal Corporate'
        INFORMAL = 'INFORMAL', 'Informal/Trader'
        STUDENT = 'STUDENT', 'Student'
        NYSC = 'NYSC', 'NYSC Corp Member'
        UNEMPLOYED = 'UNEMPLOYED', 'Unemployed'

    class IncomeBracket(models.TextChoices):
        UNDER_50K = 'UNDER_50K', 'Under ₦50,000'
        BETWEEN_50K_150K = '50K_150K', '₦50,000 - ₦150,000'
        BETWEEN_150K_300K = '150K_300K', '₦150,000 - ₦300,000'
        ABOVE_300K = 'ABOVE_300K', 'Above ₦300,000'

    NIGERIAN_STATES = [
        ('NATIONWIDE', 'Nationwide'),
        ('ABUJA', 'FCT - Abuja'),
        ('LAGOS', 'Lagos'),
        ('KANO', 'Kano'),
        ('RIVERS', 'Rivers'),
        # Add remaining Nigerian states as needed
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    account_type = models.CharField(max_length=10, choices=AccountType.choices, default=AccountType.PERSONAL)

    # Personal Profile Fields
    username_handle = models.CharField(max_length=50, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    state = models.CharField(max_length=50, choices=NIGERIAN_STATES, blank=True, null=True)
    location = models.CharField(max_length=50, choices=NIGERIAN_STATES, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices, blank=True, null=True)
    income_bracket = models.CharField(max_length=20, choices=IncomeBracket.choices, blank=True, null=True)
    education_level = models.CharField(max_length=20, choices=EducationLevel.choices, blank=True, null=True)
    employment_status = models.CharField(max_length=20, choices=EmploymentStatus.choices, blank=True, null=True)

    # Business Profile Fields
    business_name = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    year_of_incorporation = models.PositiveIntegerField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.account_type}"