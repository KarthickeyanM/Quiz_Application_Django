from django.urls import path
from .views import index ,LoginView, SignUpView, DashboardView, QuizPageView, LogoutView, ResultView

app_name = "Quiz"

urlpatterns = [
    # path("",index, name="index"),
    path("",LoginView.as_view(), name="login"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("quiz/<int:quiz_id>", QuizPageView.as_view(), name="quiz_page"),
    path('results/<int:quiz_id>/', ResultView, name='Results'),
    path("logout", LogoutView, name="logout"),
]