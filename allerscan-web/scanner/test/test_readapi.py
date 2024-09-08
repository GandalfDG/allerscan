from django.test import TestCase
from ..readapi import load_allergens, match_allergens

class ReadApiTest(TestCase):
    def setUp(self) -> None:
        self.allergens_dict = load_allergens("scanner/allergens.yaml")
        return super().setUp()
    
    def test_load_allergens(self):
        allergens = self.allergens_dict
        self.assertIn("benzoic acid", allergens.keys())
        self.assertIn("acidum benzoicun", allergens["benzoic acid"])

    def test_match_allergens(self):
        pass
