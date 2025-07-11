# Modify this in onlinecourse/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Course, Lesson, Instructor, Learner, Enrollment, Question, Choice, Submission # Add Question, Choice, Submission
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Add this to onlinecourse/views.py
@csrf_exempt
@login_required
def submit_exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    # Create a new submission object
    submission = Submission.objects.create(enrollment=enrollment)

    # Collect selected choices from the request
    # request.POST will contain data like {'choice_1': ['1', '2'], 'choice_2': ['3']}
    # where 'choice_X' is the name attribute from the form and the values are choice IDs.
    for key, value in request.POST.items():
        if key.startswith('choice_') and value: # Check if key starts with 'choice_' and has a value
            try:
                choice_id = int(value)
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
            except ValueError:
                # Handle cases where value might not be an integer (e.g., if there's no choice selected for a question)
                pass
            except Choice.DoesNotExist:
                # Handle cases where choice_id does not exist
                pass

    submission.save() # Save the many-to-many relationship

    # Redirect to the show_exam_result view
    return redirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

# ... inside submit_exam view
# Collect selected choices from the request
# Assuming 'choice_question_id' is the name for choices for a given question
# and values are choice IDs
selected_choices_ids = []
for key, value in request.POST.items():
    if key.startswith('choice_'): # Example: 'choice_123'
        # 'value' here will be the ID of the selected choice for that question
        # If multiple choices can be selected for one question, request.POST.getlist(key) would be used.
        # Given the template uses a single checkbox per choice, 'value' will be a single ID.
        try:
            selected_choices_ids.append(int(value))
        except ValueError:
            pass

# Add all selected choices to the submission
for choice_id in selected_choices_ids:
    try:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)
    except Choice.DoesNotExist:
        pass

submission.save()
# ... rest of the view

# Add this to onlinecourse/views.py
@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, enrollment__user=request.user, enrollment__course=course)

    # Get all questions for the course
    questions = course.question_set.all()

    # Get selected choices from the submission
    selected_choices = submission.choices.all()
    selected_choices_ids = [choice.id for choice in selected_choices]

    total_score = 0
    question_results = []

    for question in questions:
        # Check if the learner got the score for this question
        # Pass only the selected choice IDs that belong to this question
        choices_for_this_question = [c.id for c in question.choice_set.all() if c.id in selected_choices_ids]

        is_correct = question.is_get_score(choices_for_this_question)

        if is_correct:
            total_score += question.grade

        # Prepare data for rendering
        question_results.append({
            'question': question,
            'is_correct': is_correct,
            'selected_choices': [c for c in selected_choices if c.question == question],
            'correct_choices': question.choice_set.filter(is_correct=True),
        })

    # Define passing score (e.g., 70% of total possible grade)
    total_possible_grade = sum([q.grade for q in questions])
    passing_score = total_possible_grade * 0.7 # Example: 70%

    passed = total_score >= passing_score

    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'total_possible_grade': total_possible_grade,
        'passed': passed,
        'question_results': question_results,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)