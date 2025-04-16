from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Subcategory, Quiz
from django.shortcuts import render
from .models import Category
from .models import QuizResult
def quizzes(request):
    """View for displaying all categories"""
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'quiz/quizzes.html', {'categories': categories})


# Home Page View
def home(request):
    return render(request, 'quiz/home.html')

# Categories View
def categories(request):
    """Display all categories"""
    categories = Category.objects.all()
    return render(request, 'quiz/quizzes.html', {'categories': categories})

# Subcategories View
def subcategories(request, category_id):
    """Display subcategories of a specific category"""
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'quiz/subcategories.html', {'category': category, 'subcategories': subcategories})

# Quizzes by Subcategory View
def quizzes_by_subcategory(request, subcategory_id):
    """Display quizzes of a specific subcategory"""
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    quizzes = subcategory.quizzes.all()
    return render(request, 'quiz/subcategory_quizzes.html', {'subcategory': subcategory, 'quizzes': quizzes})

# Quiz Detail View
def quiz_detail(request, quiz_id):
    """Display a specific quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

# Quiz Attempt View (Requires Login)
@login_required
def quiz_attempt(request, quiz_id):
    """Attempt a specific quiz (restricted to logged-in users)"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_attempt.html', {'quiz': quiz})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('quizzes')  # Redirect to quizzes page after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'quiz/login.html', {'form': form})

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}, your account has been created!")
            return redirect('quizzes')  # Redirect to quizzes page after signup
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'quiz/signup.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

from django.shortcuts import render, get_object_or_404
from .models import Quiz

def quiz_questions(request, quiz_id):
    """Display questions for a specific quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Fetch all questions for the quiz
    return render(request, 'quiz/quiz_questions.html', {'quiz': quiz, 'questions': questions})

from django.http import JsonResponse

def submit_quiz(request, quiz_id):
    """Handle submission of quiz answers"""
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = question.options.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 1

        return JsonResponse({'score': score, 'total_questions': total_questions})
from django.shortcuts import render, get_object_or_404
from .models import Quiz

@login_required
def quiz_attempt(request, quiz_id):
    """Display questions for a specific quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Fetch all questions for the quiz
    return render(request, 'quiz/quiz_attempt.html', {'quiz': quiz, 'questions': questions})
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404
from .models import Quiz, QuizResult

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    results = []
    score = 0
    time_taken = int(request.POST.get('time_taken', 0)) if request.method == 'POST' else 0

    if request.method == 'POST':
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            selected_option = None
            correct_option = question.options.filter(is_correct=True).first()
            if selected_option_id:
                selected_option = question.options.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 1
            # Only append incorrect answers
            if not (selected_option and selected_option.is_correct):
                results.append({
                    'question': question,
                    'selected_option': selected_option,
                    'correct_option': correct_option,
                })

        # Save the result for leaderboard
        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            time_taken=time_taken
        )

        # Calculate user rank
        user_rank = QuizResult.objects.filter(
            quiz=quiz,
            score__gt=score
        ).count() + 1

        return render(request, 'quiz/submit_quiz.html', {
            'quiz': quiz,
            'score': score,
            'total_questions': questions.count(),
            'results': results,
            'time_taken': time_taken,
            'user_rank': user_rank
        })

def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    results = QuizResult.objects.filter(quiz=quiz).order_by('-score', 'time_taken')[:20]
    return render(request, 'quiz/leaderboard.html', {
        'quiz': quiz,
        'results': results
    })