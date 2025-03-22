from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz

def quiz_list(request):
    # Show all quizzes
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

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
        
        return render(request, 'quiz/quiz_result.html', context)
    
    return redirect('quiz_list')

def quiz_submit_all(request):
    if request.method == 'POST':
        # Get all quiz IDs from the form
        quiz_ids = request.POST.getlist('quiz_ids')
        
        # Process each quiz answer
        results = []
        correct_count = 0
        
        for quiz_id in quiz_ids:
            quiz = get_object_or_404(Quiz, id=quiz_id)
            selected_option = request.POST.get(f'answer_{quiz_id}')
            
            # Check if the answer is correct
            is_correct = selected_option == quiz.answer
            if is_correct:
                correct_count += 1
            
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
            
            # Get the text of the correct option
            if quiz.answer == 'option1':
                correct_option_text = quiz.option1
            elif quiz.answer == 'option2':
                correct_option_text = quiz.option2
            elif quiz.answer == 'option3':
                correct_option_text = quiz.option3
            else:
                correct_option_text = quiz.option4
            
            # Add to results
            results.append({
                'quiz': quiz,
                'selected_option': selected_option,
                'selected_text': selected_option_text,
                'correct_text': correct_option_text,
                'is_correct': is_correct
            })
        
        context = {
            'results': results,
            'correct_count': correct_count,
            'total_questions': len(quiz_ids)
        }
        
        return render(request, 'quiz/quiz_results.html', context)
    
    return redirect('quiz_list')
