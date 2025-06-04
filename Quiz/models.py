from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_name = models.CharField(max_length=100)
    quiz_description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50)  # e.g., 'MCQ', 'True/False', 'Short Answer'

    def __str__(self):
        return f"Question {self.question_id} for {self.quiz.quiz_name}"

class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option {self.option_id} for Question {self.question.question_id}"
    
class response(models.Model):
    response_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"Response {self.response_id} by {self.user.username} for Question {self.question.question_id}"
    
class quiz_result(models.Model):
    result_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()

    def __str__(self):
        return f"Result {self.result_id} for {self.user.username} in {self.quiz.quiz_name}"
    
