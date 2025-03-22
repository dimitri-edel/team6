from django.test import TestCase
from about.models import About
from category.models import Category

class AboutModelTest(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name="Computer Science")
        
        # Create a test About instance
        self.about = About.objects.create(
            name="Grace Hopper",
            birth_date="1906",
            contribution="Computer scientist and pioneer in programming.",
            category=self.category
        )
    
    def test_about_creation(self):
        """Test that About object can be created with basic fields"""
        self.assertEqual(self.about.name, "Grace Hopper")
        self.assertEqual(self.about.birth_date, "1906")
        self.assertTrue(self.about.contribution)
        self.assertEqual(self.about.category, self.category)
    
    def test_string_representation(self):
        """Test that the string representation is the name field"""
        self.assertEqual(str(self.about), "Grace Hopper")
    
    def test_category_relationship(self):
        """Test that the relationship with Category works correctly"""
        # Get all profiles in the category
        profiles_in_category = self.category.about_profiles.all()
        self.assertIn(self.about, profiles_in_category)
