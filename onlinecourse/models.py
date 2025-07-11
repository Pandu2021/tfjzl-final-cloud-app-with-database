# onlinecourse/models.py

from django.db import models
from django.contrib.auth.models import User

# Existing models (assuming these are already defined in your file)
# If these are not present, you need to ensure they are defined or imported.
# For the purpose of fixing the NameError, we'll assume they exist prior to Question model.

class Course(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateField()
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    mode = models.CharField(max_length=30, default='audit')
    # Additional fields could be added here, such as 'completion_status'

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.name}'

# New Models for Final Project
# Question Model: Stores questions for an exam with a Many-To-One relationship to a course.
# It includes the question text and a score value.
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=0) # Score for the question

    def __str__(self):
        return self.question_text

    # Method to calculate if the learner gets the score of the question
    # This checks if all correct choices for the question are among the selected IDs.
    def is_get_score(self, selected_ids):
        # Count all correct answers for this question
        all_correct_choices = self.choice_set.filter(is_correct=True).count()
        # Count how many of the selected choices are correct for this question
        selected_correct_choices = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        # If the number of all correct choices matches the number of selected correct choices,
        # the learner gets the full score for this question.
        if all_correct_choices == selected_correct_choices and all_correct_choices > 0:
            return True
        else:
            return False

# Choice Model: Stores choices for a question.
# It has a Many-to-One relationship to the Question model, choice text, and a boolean
# indicating if it's the correct answer.
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

# Submission Model: Records a learner's exam submission for a specific enrollment.
# It has a Many-to-One relationship with Enrollment and a Many-to-Many relationship with Choice,
# allowing it to track all choices selected by the learner for an exam.
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.enrollment.user.username} on {self.enrollment.course.name} at {self.submission_date.strftime('%Y-%m-%d %H:%M')}"
        
        