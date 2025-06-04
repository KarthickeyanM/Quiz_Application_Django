# insert_questions.py
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from Quiz.models import Quiz, Question, Option

quiz = Quiz.objects.first()
if not quiz:
    raise Exception("No quiz found. Create a quiz first.")

for i in range(1, 11):
    q_text = f"What is the answer to question {i}?"
    question = Question.objects.create(
        quiz=quiz,
        question_text=q_text,
        question_type='MCQ'
    )

    correct_option = random.randint(1, 4)
    for j in range(1, 5):
        option = Option.objects.create(
            question=question,
            option_text=f"Option {j} for Q{i}",
            is_correct=(j == correct_option)
        )
        print(f"Created Option: {option.option_text} (Correct: {option.is_correct}) for Q{i}")

print("✅ 10 questions with 4 options each created successfully.")
