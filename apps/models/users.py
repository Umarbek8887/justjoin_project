from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, PositiveSmallIntegerField, BooleanField, FileField, Model, ForeignKey, CASCADE, \
    Q
from django.db.models.constraints import CheckConstraint
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, TextField, EmailField

from apps.managers import CustomUserManager


class JobPosition(TextChoices):
    FRONTEND_DEVELOPER = "frontend developer", "Frontend Developer"
    FRONTEND_DEVELOPER_REACT = "frontend developer react", "Frontend Developer React"
    FRONTEND_DEVELOPER_VUE_JS = "frontend developer vue_js", "Frontend Developer Vue.Js"
    FRONTEND_DEVELOPER_ANGULAR = "frontend developer angular", "Frontend Developer Angular"
    SENIOR_FRONTEND_DEVELOPER_ANGULAR = "senior frontend developer angular", "Senior Frontend Developer Angular"
    SENIOR_FRONTEND_DEVELOPER = "senior frontend developer", "Senior Frontend Developer"

    BACKEND_DEVELOPER = "backend developer", "Backend Developer"
    SENIOR_BACKEND_DEVELOPER = "senior backend developer", "Senior Backend Developer"
    JAVA_BACKEND_DEVELOPER = "java backend developer", "Java Backend Developer"

    FULLSTACK_DEVELOPER = "fullstack developer", "Fullstack Developer"

    SOFTWARE_ENGINEER = "software engineer", "Software Engineer"
    PRINCIPAL_SOFTWARE_ENGINEER = "principal software engineer", "Principal Software Engineer"
    LEAD_SOFTWARE_ENGINEER = "lead software engineer", "Lead Software Engineer"
    FRONTEND_SOFTWARE_ENGINEER = "frontend software engineer", "Frontend Software Engineer"
    BACKEND_SOFTWARE_ENGINEER = "backend software engineer", "Backend Software Engineer"
    SOFTWARE_ENGINEER_BACKEND = "software engineer backend", "Software Engineer Backend"
    SENIOR_BACKEND_SOFTWARE_ENGINEER = "senior backend software engineer", "Senior Backend Software Engineer"
    FULLSTACK_SOFTWARE_ENGINEER = "fullstack software engineer", "Fullstack Software Engineer"
    SENIOR_SOFTWARE_ENGINEER = "senior software engineer", "Senior Software Engineer"
    SENIOR_EMBEDDED_SOFTWARE_ENGINEER = "senior embedded software engineer", "Senior Embedded Software Engineer"

    PROJECT_MANAGER = "project manager", "Project Manager"
    PMO_PROJECT_MANAGER = "pmo project manager", "PMO Project Manager"
    IT_PROJECT_MANAGER = "it project manager", "IT Project Manager"
    SENIOR_PROJECT_MANAGER = "senior project manager", "Senior Project Manager"

    SOFTWARE_TESTER = "software tester", "Software Tester"

    DATA_ANALYST = "data analyst", "Data Analyst"
    SENIOR_DATA_ANALYST = "senior data analyst", "Senior Data Analyst"
    TRAINEE_DATA_ANALYST = "trainee data analyst", "Trainee Data Analyst"

    DEVOPS_ENGINEER = "devops engineer", "Devops Engineer"
    KUBERNETES_DEVOPS_ENGINEER = "kubernetes devops engineer", "Kubernetes Devops Engineer"
    PLATFORM_DEVOPS_ENGINEER = "platform devops engineer", "Platform Devops Engineer"
    SENIOR_DEVOPS_ENGINEER = "senior devops engineer", "Senior Devops Engineer"
    CLOUD_DEVOPS_ENGINEER = "cloud devops engineer", "Cloud Devops Engineer"
    LEAD_DEVOPS_ENGINEER = "lead devops engineer", "Lead Devops Engineer"

    DATA_ENGINEER = "data engineer", "Data Engineer"
    SENIOR_DATA_ENGINEER = "senior data engineer", "Senior Data Engineer"
    SYNTHETIC_DATA_ENGINEER = "synthetic data engineer", "Synthetic Data Engineer"

    AUTOMATION_QA_ENGINEER = "automation qa engineer", "Automation QA Engineer"


class SituationType(TextChoices):
    I_NEED_A_JOB_ASAP = "i need a job asap", "I need a job ASAP"
    I_AM_OPEN_TO_OFFERS = "i'm open to offers", "I'm open to offers"
    I_AM_LOOKING_FOR_A_NEW_JOB_NOW = "i'm not looking for a new job now", "I'm not looking for a new job now"


class AvailabilityAfter(TextChoices):
    RIGHT_AWAY = "right away", "Right away"
    IN_1_WEEK = "in 1 week", "In 1 week"
    IN_2_WEEKS = "in 2 weeks", "In 2 weeks"
    IN_ABOUT_A_MONTH = "in about a month", "In about a month"
    IN_2_MONTHS = "in 2 months", "In 2 months"
    IN_3_MONTHS = "in 3 months", "In 3 months"


class TechStacks(TextChoices):
    DOT_NET = ".net", ".NET"
    C_SHARP = "c#", "C#"
    SQL = "sql", "SQL"
    TYPESCRIPT = "typescript", "TypeScript"
    JAVASCRIPT = "javascript", "JavaScript"
    DOT_NET_C_SHARP = ".net_c#", ".NET C#"
    REACT = "react", "React"
    AZURE = "azure", "Azure"
    ANDROID = "android", "Android"
    CI_CD = "ci_cd", "CI/CD"
    ASP_NET = "asp_net", "ASP.NET"
    REST_API = "rest_api", "REST API"
    IOS = "ios", "iOS"
    ASP_NET_CORE = "asp_net_core", "ASP.NET Core"
    KOTLIN = "kotlin", "Kotlin"
    RABBITMQ = "rabbitmq", "RabbitMQ"
    ANGULAR = "angular", "Angular"
    DOT_NET_CORE = ".net_core", ".NET Core"
    GIT = "git", "Git"
    REACT_NATIVE = "react_native", "React Native"
    ENTITY_FRAMEWORK = "entity_framework", "Entity Framework"
    POSTGRESQL = "postgresql", "PostgreSQL"
    DOCKER = "docker", "Docker"
    SQL_SERVER = "sql_server", "SQL Server"
    ANDROID_SDK = "android_sdk", "Android SDK"
    MVVM = "mvvm", "MVVM"
    SWIFT = "swift", "Swift"
    FLUTTER = "flutter", "Flutter"
    SWIFT_UI = "swiftui", "SwiftUI"
    JAVA = "java", "Java"
    UI_KIT = "uikit", "UIKit"
    COROUTINES = "coroutines", "Coroutines"
    KOTLIN_MULTIPLATFORM = "kotlin_multiplatform", "Kotlin Multiplatform"
    BLUETOOTH_LOW_ENERGY = "bluetooth_le", "Bluetooth Low Energy"


class CandidateUser(AbstractUser):
    email = EmailField("email address", unique=True)
    is_active = BooleanField(default=False)
    username = None
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    github_link = CharField(max_length=255, null=True, blank=True)
    linkedin_link = CharField(max_length=255, null=True, blank=True)
    other_link = CharField(max_length=255, null=True, blank=True)
    message_to_employee = TextField(null=True)
    image = ImageField(upload_to='media/profile-avatar/%Y/%m/%d')
    current_position = CharField(choices=JobPosition.choices, max_length=128, default=JobPosition.FRONTEND_DEVELOPER)
    years_of_exp = PositiveSmallIntegerField(default=0, db_default=0)
    location = CharField(max_length=128, null=True)
    native_lang = CharField(max_length=128, null=True)
    job_status = CharField(choices=SituationType.choices, max_length=128, default=SituationType.I_NEED_A_JOB_ASAP)
    availability_after = CharField(choices=AvailabilityAfter.choices, max_length=20,
                                   default=AvailabilityAfter.RIGHT_AWAY)
    cv_file = FileField(upload_to='media/cv/%Y/%m/%d', null=True, blank=True)


class CandidateOtherPositions(Model):
    position = CharField(choices=JobPosition.choices, max_length=128, default=JobPosition.FRONTEND_DEVELOPER)
    candidate_user = ForeignKey('apps.CandidateUser', CASCADE, related_name='candidate_other_positions')


class CandidateSkills(Model):
    tech_stack = CharField(choices=TechStacks.choices, max_length=128, default=TechStacks.DOT_NET)
    level = PositiveSmallIntegerField(default=0, db_default=0)
    candidate_user = ForeignKey('apps.CandidateUser', CASCADE, related_name='candidate_other_positions')

    class Meta:
        verbose_name = 'Candidate Skill'
        verbose_name_plural = 'Candidate Skills'
        constraints = [
            CheckConstraint(condition=Q(level__gte=0) & Q(level__lte=5),
                            name="level_gte_0_lte_5",
                            violation_error_message="Level must be between 0 and 5")
        ]



