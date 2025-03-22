from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz

def quiz_list(request):
    # Show all quizzes
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        selected_option = request.POST.get('answer')
        
        # Get the text of the selected option
        if selected_option == 'option1':
            selected_option_text = quiz.option1
        elif selected_option == 'option2':
            selected_option_text = quiz.option2
        elif selected_option == 'option3':
            selected_option_text = quiz.option3
        elif selected_option == 'option4':
            selected_option_text = quiz.option4
        else:
            selected_option_text = "No option selected"
        
        # Check if answer is correct
        is_correct = selected_option == quiz.answer
        
        # Get the correct answer text
        if quiz.answer == 'option1':
            correct_option_text = quiz.option1
        elif quiz.answer == 'option2':
            correct_option_text = quiz.option2
        elif quiz.answer == 'option3':
            correct_option_text = quiz.option3
        else:
            correct_option_text = quiz.option4
        
        context = {
            'quiz': quiz,
            'selected_option_text': selected_option_text,
            'correct_option_text': correct_option_text,
            'is_correct': is_correct,
        }
        
        return render(request, 'quiz_result.html', context)
    
    return redirect('quiz_list')
