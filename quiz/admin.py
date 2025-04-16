from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Subcategory, Quiz,Question,Option,QuizResult


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizResult)