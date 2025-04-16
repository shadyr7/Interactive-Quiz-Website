from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        verbose_name_plural = "Subcategories"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=300)  # Time limit in seconds (5 minutes default)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Quizzes"
class Question(models.Model):
    text = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    def __str__(self):
        return self.text

class Option(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)  # Indicates if this option is correct

    def __str__(self):
        return self.text
from django.contrib.auth.models import User

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    time_taken = models.IntegerField()  # Time taken in seconds
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score', 'time_taken', '-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
