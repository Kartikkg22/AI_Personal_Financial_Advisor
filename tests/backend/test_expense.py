import unittest
from backend.app.services.expense import categorize_expense

class TestExpenseCategorization(unittest.TestCase):
    def test_categorize_expense(self):
        self.assertEqual(categorize_expense("Uber Ride"), "Transportation")
        self.assertEqual(categorize_expense("Starbucks Coffee"), "Food & Beverage")
        self.assertEqual(categorize_expense("Unknown Transaction"), "Other")

if __name__ == '__main__':
    unittest.main()
