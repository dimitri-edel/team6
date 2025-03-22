from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.middleware.csrf import get_token
from .models import Quiz

def quiz_list(request):
    # Reset session data when starting a new quiz
    if 'quiz_progress' in request.session:
        del request.session['quiz_progress']
    if 'quiz_results' in request.session:
        del request.session['quiz_results']
    
    # Redirect to the first question
    quizzes = Quiz.objects.all().order_by('id')
    if quizzes:
        return redirect('quiz_question', quiz_id=quizzes.first().id)
    else:
        return HttpResponse("<h1>No quizzes available</h1>")

def quiz_question(request, quiz_id):
    # Get the current quiz
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Initialize quiz progress in session if not present
    if 'quiz_progress' not in request.session:
        request.session['quiz_progress'] = []
    
    if 'quiz_results' not in request.session:
        request.session['quiz_results'] = []
    
    # Create HTML directly
    csrf_token = get_token(request)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz Question</title>
    </head>
    <body>
        <h1>{quiz.about.name} Quiz</h1>
        <h2>Question {len(request.session['quiz_progress']) + 1}</h2>
        
        <h3>{quiz.question}</h3>
        
        <form method="post" action="/quizzes/{quiz.id}/answer/">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            
            <div>
                <input type="radio" name="answer" id="option1" value="option1" required>
                <label for="option1">{quiz.option1}</label>
            </div>
            <div>
                <input type="radio" name="answer" id="option2" value="option2">
                <label for="option2">{quiz.option2}</label>
            </div>
            <div>
                <input type="radio" name="answer" id="option3" value="option3">
                <label for="option3">{quiz.option3}</label>
            </div>
            <div>
                <input type="radio" name="answer" id="option4" value="option4">
                <label for="option4">{quiz.option4}</label>
            </div>
            
            <button type="submit">Submit Answer</button>
        </form>
    </body>
    </html>
    """
    
    return HttpResponse(html)

def quiz_answer(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        selected_option = request.POST.get('answer')
        
        # Check if the answer is correct
        is_correct = selected_option == quiz.answer
        
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
        
        # Store the result in session
        if 'quiz_progress' not in request.session:
            request.session['quiz_progress'] = []
        
        if 'quiz_results' not in request.session:
            request.session['quiz_results'] = []
        
        request.session['quiz_progress'].append(quiz.id)
        
        result = {
            'quiz_id': quiz.id,
            'question': quiz.question,
            'selected_option': selected_option,
            'selected_text': selected_option_text,
            'correct_text': correct_option_text,
            'is_correct': is_correct
        }
        
        request.session['quiz_results'].append(result)
        request.session.modified = True
        
        # Find the next quiz that hasn't been answered yet
        next_quiz = Quiz.objects.exclude(id__in=request.session['quiz_progress']).order_by('id').first()
        
        if next_quiz:
            # Show feedback for current answer and link to next question
            csrf_token = get_token(request)
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Answer Feedback</title>
            </head>
            <body>
                <h1>Question {len(request.session['quiz_progress'])}</h1>
                <h2>{quiz.question}</h2>
                
                <p><strong>Your answer:</strong> {selected_option_text}</p>
                
                {f'<p><strong>Correct!</strong> Great job!</p>' if is_correct else 
                f'<p><strong>Incorrect.</strong> The correct answer was: {correct_option_text}</p>'}
                
                <form method="get" action="/quizzes/{next_quiz.id}/">
                    <button type="submit">Next Question</button>
                </form>
            </body>
            </html>
            """
            
            return HttpResponse(html)
        else:
            # All questions have been answered, show final results
            return redirect('quiz_results')
    
    return redirect('quiz_question', quiz_id=quiz_id)

def quiz_results(request):
    # Get results from session
    if 'quiz_results' not in request.session:
        return redirect('quiz_list')
    
    results = request.session['quiz_results']
    
    # Count correct answers
    correct_count = sum(1 for result in results if result['is_correct'])
    
    # Create HTML directly
    results_html = ""
    for result in results:
        results_html += f"""
        <div>
            <h3>Question {results.index(result) + 1}</h3>
            <h4>{result['question']}</h4>
            
            <p><strong>Your answer:</strong> {result['selected_text']}</p>
            
            {f'<p><strong>Correct!</strong> Great job!</p>' if result['is_correct'] else 
            f'<p><strong>Incorrect.</strong> The correct answer was: {result["correct_text"]}</p>'}
        </div>
        <hr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz Results</title>
    </head>
    <body>
        <h1>Quiz Results</h1>
        
        <div>
            <h2>Your Score: {correct_count} out of {len(results)}</h2>
            
            {results_html}
            
            <a href="/quizzes/">Take Quiz Again</a>
        </div>
    </body>
    </html>
    """
    
    # Clear session data
    if 'quiz_progress' in request.session:
        del request.session['quiz_progress']
    if 'quiz_results' in request.session:
        del request.session['quiz_results']
    
    return HttpResponse(html)
