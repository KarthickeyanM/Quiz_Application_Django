from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from django.urls import reverse
from .models import User, Quiz, Question, Option, response, quiz_result
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        data = request.POST.dict()
        username = data.get('username')
        password = data.get('password')
        
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Django's login method
                request.session['user_id'] = user.id
                return redirect(reverse('Quiz:dashboard'))
            else:
                raise Exception("Invalid credentials")
        except User.DoesNotExist:
            return render(request, 'login.html', {'message': 'Invalid credentials! Please try again.'})
    

class SignUpView(View):
    def get(self,request):
        return render(request, 'signup.html')
    def post(self, request):
        data = request.POST.dict()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect(reverse('Quiz:login'))  # Redirect to login page after successful signup
        except Exception as e:
            return render(request, 'signup.html', {'message': 'Error creating account. Please try again.'})
        


class DashboardView(View):
    def get(self,request):
        quizzes =  Quiz.objects.all()
        return render(request,"home.html", {"quizzes": quizzes})

class QuizPageView(View):
    def get(self, request, quiz_id):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect(reverse('Quiz:login'))  # Redirect to login if not logged in

        quiz = Quiz.objects.get(quiz_id=quiz_id)
        attempted_questions = response.objects.filter(quiz=quiz, user_id=user_id).values_list('question_id', flat=True)
        

        # Get all questions in the quiz
        questions = Question.objects.filter(quiz=quiz).exclude(question_id__in=attempted_questions)

        if not questions.exists():
            return render(request, 'Quiz_question.html', {
                'quiz': quiz,
                'message': 'No questions available for this quiz.'
            })

        # # Get questions the user has already answered
        # answered_q_ids = response.objects.filter(
        #     user_id=user_id
        # ).values_list('question_id', flat=True)

        # # Get the next unanswered question
        # unanswered_questions = all_questions.exclude(id__in=answered_q_ids)

        # if not unanswered_questions.exists():
        #     # All questions answered — redirect to results
        #     return redirect(reverse('Quiz:Results') + f'?quiz_id={quiz.id}')

        # Use Paginator to fetch first unanswered question
        paginator = Paginator(questions, 1)
        try:
            page_no = int(request.GET.get('page', 1))
            if page_no < 1:
                raise ValueError()
        except (ValueError, TypeError):
            page_no = 1
        if page_no is None or page_no > paginator.num_pages:
            return redirect(reverse('Quiz:Results', kwargs={'quiz_id': quiz.quiz_id}))
        page_obj = paginator.get_page(page_no)
        current_question = page_obj.object_list[0]

        # Get choices for this question
        choices = Option.objects.filter(question=current_question)
        print(f"Choices for question {current_question.question_id}: {choices}")

        return render(request, 'Quiz_question.html', {
            'quiz': quiz,
            'question': current_question,
            'choices': choices,
        })
    # def get(self, request, quiz_id):
    #     quiz = Quiz.objects.get(id=quiz_id)
    #     user_id = request.session.get('user_id')
    #     questions = question.objects.filter(quiz=quiz)
    #     if not questions:
    #         return render(request, 'quiz_detail.html', {'quiz': quiz, 'message': 'No questions available for this quiz.'})
    #     questions_to_answer = question.objects.filter(quiz=quiz).exclude(question_id=response.objects.filter(user_id=user_id).values_list('question_id', flat=True))
    #     if not questions_to_answer:
    #         return redirect(reverse('Quiz:Results'), {'quiz_id': quiz.id})  # Redirect to results if no questions left to answer
    #     question = Paginator(questions, 1)
    #     choices = option.objects.filter(question_id=question.get_page(1).id) #.object_list[0]
    #     if not questions:
    #         return render(request, 'quiz_detail.html', {'quiz': quiz, 'message': 'No questions available for this quiz.'})
    #     return render(request, 'quiz_detail.html', {'quiz': quiz, 'question': question, 'choices': choices})
    
    def post(self, request, quiz_id):
        data = request.POST.dict()
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        user = User.objects.get(id=request.session['user_id'])
        question = Question.objects.get(question_id=data.get('question_id'))
        
        selected_option = Option.objects.get(option_id=data.get('option_id'))

        # Save the response
        response_obj = response(quiz=quiz, user=user, question=question, selected_option=selected_option)
        response_obj.save()

        return redirect(reverse('Quiz:quiz_page', args=[quiz_id])+ f'?page={int(data.get("page", 1)) + 1}')  # Redirect to next question

def LogoutView(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    logout(request)
    return redirect(reverse('Quiz:login'))  # Redirect to login page after logout

def ResultView(request, quiz_id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)

    responses = response.objects.filter(quiz=quiz, user=user)
    
    if not responses.exists():
        return render(request, 'results.html', {
            'quiz': quiz,
            'message': 'No responses found for this quiz.'
        })

    total_questions = responses.count()
    correct_answers = responses.filter(selected_option__is_correct=True)
    correct_answers_count = correct_answers.count()
    print(correct_answers_count, total_questions)
    score = (correct_answers_count / total_questions) * 100 if total_questions > 0 else 0

    return render(request, 'results.html', {
        'quiz': quiz,
        'user': user,
        'score': score,
        'total_questions': total_questions,
        'correct_answers': correct_answers_count,
    })