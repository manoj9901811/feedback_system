from django.db import models

# Subject model
class Subject(models.Model):
    name = models.CharField(max_length=100, default="Untitled Subject")
    code = models.CharField(max_length=20, default="SUB001")
    semester = models.CharField(max_length=10, default="1")

    def __str__(self):
        return self.name

# Faculty model
class Faculty(models.Model):
    user = models.CharField(max_length=150, default="faculty_user")
    name = models.CharField(max_length=100, default="Faculty Name")
    usn = models.CharField(max_length=20, default="FAC123")
    section = models.CharField(max_length=10, default="A")
    year = models.IntegerField(default=2019)
    subjects = models.ManyToManyField(Subject)
    semester = models.CharField(max_length=10, default="1")  # ✅ must be here


    def __str__(self):
        return self.name

# Student model
import random
import string
from django.db import models

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class Student(models.Model):
    user = models.CharField(max_length=150)
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20)
    section = models.CharField(max_length=10, default="A")
    year = models.IntegerField(default=2020)
    semester = models.CharField(max_length=10, default="1")

    # Random credentials fields
    generated_userid = models.CharField(max_length=150, blank=True)
    generated_password = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.generated_userid:
            self.generated_userid = generate_random_string(6)
        if not self.generated_password:
            self.generated_password = generate_random_string(8)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



# Section model
class Section(models.Model):
    name = models.CharField(max_length=50, unique=True, default='A')

    def __str__(self):
        return self.name

# Student-Subject Mapping model
class StudentSubject(models.Model):
    student_name = models.CharField(max_length=100, default='Unnamed Student')
    subject_name = models.CharField(max_length=100, default='Default Subject')

    def __str__(self):
        return f"{self.student_name} - {self.subject_name}"

# Student-Faculty Mapping model
class StudentFacultyMap(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True, default=None)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        if self.student and self.faculty:
            return f"{self.student.name} → {self.faculty.name}"
        return "Mapping (incomplete)"

# Feedback Question model
class FeedbackQuestion(models.Model):
    text = models.TextField(default="How was the teaching?")

    def __str__(self):
        return self.text

# Feedback model
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=1)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=1)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    question = models.ForeignKey(FeedbackQuestion, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(default=3)  # 1 to 5 scale
    comments = models.TextField(blank=True, null=True, default='No comments')

    def __str__(self):
        return f"{self.student.name} rated {self.faculty.name}: {self.rating}"

class FacultySubject(models.Model):
    faculty_name = models.CharField(max_length=100, default='A')
    subject_name = models.CharField(max_length=100, default='A')
    semester = models.CharField(max_length=10, default='1')
    section = models.CharField(max_length=10, default='A')
    year = models.CharField(max_length=10, default='2025')

    def __str__(self):
        return f"{self.faculty_name} - {self.subject_name} ({self.semester}{self.section}, {self.year})"
    
class Facility(models.Model):
    text = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.text


class FacilityFeedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # 0 can mean "not rated yet"


class CourseEndQuestion(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class CourseEndFeedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(CourseEndQuestion, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)  # Default rating is 3 (e.g., 'Good')
