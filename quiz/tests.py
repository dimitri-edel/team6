from django.test import TestCase
from quiz.models import Quiz
from about.models import About
from category.models import Category

class QuizModelTest(TestCase):
    def setUp(self):
        # Create test category
        self.category = Category.objects.create(name="Computer Science")
        
        # Create test About instance
        self.about = About.objects.create(
            name="Ada Lovelace",
            birth_date="1815",
            contribution="First computer programmer.",
            category=self.category
        )
        
        # Create test Quiz instance
        self.quiz = Quiz.objects.create(
            about=self.about,
            question="In what year was Ada Lovelace born?",
            option1="1805",
            option2="1815",
            option3="1825",
            option4="1835",
            answer="option2"
        )
    
    def test_quiz_creation(self):
        """Test that Quiz object can be created with all required fields"""
        self.assertEqual(self.quiz.about, self.about)
        self.assertEqual(self.quiz.question, "In what year was Ada Lovelace born?")
        self.assertEqual(self.quiz.option1, "1805")
        self.assertEqual(self.quiz.option2, "1815")
        self.assertEqual(self.quiz.option3, "1825")
        self.assertEqual(self.quiz.option4, "1835")
        self.assertEqual(self.quiz.answer, "option2")
    
    def test_string_representation(self):
        """Test that the string representation shows the related About name"""
        self.assertEqual(str(self.quiz), "Quiz for Ada Lovelace")
    
    def test_relationship_with_about(self):
        """Test that the relationship with About model works correctly"""
        # Check that the quiz is in the about's quizzes
        quizzes = self.about.quizzes.all()
        self.assertIn(self.quiz, quizzes)
        
        # Test cascade delete - if About is deleted, related Quiz should be deleted
        self.about.delete()
        self.assertEqual(Quiz.objects.filter(id=self.quiz.id).count(), 0)
