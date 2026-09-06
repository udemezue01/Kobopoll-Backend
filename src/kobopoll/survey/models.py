from django.db import models
from django.conf import settings


class Survey(models.Model):
    # Demographics and targeting choices
    class EducationLevel(models.TextChoices):
        ANY = "ANY", "Any Education Level"
        O_LEVEL = "O_LEVEL", "O'Level (WAEC/NECO)"
        OND_HND = "OND_HND", "OND/HND"
        BACHELORS = "BACHELORS", "Bachelor's Degree"

    class EmploymentStatus(models.TextChoices):
        ANY = "ANY", "Any Status"
        FORMAL = "FORMAL", "Formal Corporate"
        INFORMAL = "INFORMAL", "Informal/Trader"
        STUDENT = "STUDENT", "Student"
        NYSC = "NYSC", "NYSC Corp Member"
        UNEMPLOYED = "UNEMPLOYED", "Unemployed"

    class IncomeBracket(models.TextChoices):
        ANY = "ANY", "Any Income"
        UNDER_50K = "UNDER_50K", "Under ₦50,000"
        BETWEEN_50K_150K = "50K_150K", "₦50,000 - ₦150,000"
        ABOVE_150K = "ABOVE_150K", "Above ₦150,000"

    NIGERIAN_STATES = [
        ("NATIONWIDE", "Nationwide"),
        ("LAGOS", "Lagos"),
        ("ABUJA", "FCT - Abuja"),
        ("KANO", "Kano"),
        ("RIVERS", "Rivers"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="surveys"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Demographic Filters
    min_age = models.PositiveIntegerField(default=18)
    max_age = models.PositiveIntegerField(default=100)
    business_sector = models.CharField(max_length=100, blank=True)
    location = models.CharField(
        max_length=50, choices=NIGERIAN_STATES, default="NATIONWIDE"
    )
    income_bracket = models.CharField(
        max_length=20, choices=IncomeBracket.choices, default=IncomeBracket.ANY
    )
    education_level = models.CharField(
        max_length=20, choices=EducationLevel.choices, default=EducationLevel.ANY
    )
    employment_status = models.CharField(
        max_length=20, choices=EmploymentStatus.choices, default=EmploymentStatus.ANY
    )

    # Pricing & Metrics
    cost_per_response = models.DecimalField(max_digits=10, decimal_places=2)
    total_respondents_needed = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(
        null=True, blank=True, help_text="Leave blank for an unending survey"
    )

    def save(self, *args, **kwargs):
        # Automatically calculates total cost before saving
        self.total_cost = self.cost_per_response * self.total_respondents_needed
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.survey.title} - {self.text}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text


class Response(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responses"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="responses"
    )
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "question",
        )  # Prevents duplicate answers per question

    def __str__(self):
        return f"{self.user.email} - {self.question.id}"
