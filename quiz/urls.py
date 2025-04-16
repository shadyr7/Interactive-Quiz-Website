from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('quizzes/', views.quizzes, name='quizzes'),  # All quizzes/categories
    path('category/<int:category_id>/', views.subcategories, name='subcategories'),  # Subcategories for a category
    path('subcategory/<int:subcategory_id>/', views.quizzes_by_subcategory, name='subcategory_quizzes'),  # Quizzes in a subcategory
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),  # Quiz detail page
    path('quiz/<int:quiz_id>/attempt/', views.quiz_attempt, name='quiz_attempt'),  # Quiz attempt page
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('logout/', views.logout_view, name='logout'),  # Logout functionality
    
    path('quiz/<int:quiz_id>/questions/', views.quiz_questions, name='quiz_questions'),
    
    path('quiz/<int:quiz_id>/attempt/', views.quiz_attempt, name='quiz_attempt'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


