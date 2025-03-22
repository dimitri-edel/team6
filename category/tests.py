from django.test import TestCase
from category.models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name="2000s–Present – Women Shaping Modern Tech")
    
    def test_category_creation(self):
        """Test that Category object can be created with name field"""
        self.assertEqual(self.category.name, "2000s–Present – Women Shaping Modern Tech")
    
    def test_string_representation(self):
        """Test that the string representation is the name field"""
        self.assertEqual(str(self.category), "2000s–Present – Women Shaping Modern Tech")
    
    def test_name_max_length(self):
        """Test that name field has correct max_length"""
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
