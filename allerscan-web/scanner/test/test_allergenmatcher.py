from django.test import TestCase
from ..allergenmatcher import AllergenMatcher

class AllergenMatcherTest(TestCase):
    def setUp(self):
        self.matcher = AllergenMatcher("scanner/allergens.yaml")

    def test_load_allergens(self):
        allergen_dict: dict[str, list[str]] = self.matcher.get_allergen_dict()
        self.assertIn("balsam of peru", allergen_dict)
        self.assertIn("phenylcarbinol", allergen_dict["benzyl alcohol"])

    def test_match_allergen_exact(self):
        ingredients = '''
        INGREDIENTS: 1101897 FS3 AQUA / WATER / EAU, SODIUM LAURETH SULFATE, 
        GLYCOL\nDISTEARATE, SODIUM CHLORIDE, COCAMIDOPROPYL BETAINE, 
        DIMETHICONE, COCAMIDE MEA,\nPARFUM / FRAGRANCE, CITRIC ACID, 
        SODIUM BENZOATE, SODIUM HYDROXIDE, BENZYL ALCOHOL, HEXYLENE\nGLYCOL, COCO-BETAINE, 
        AMODIMETHICONE, SALICYLIC ACID, CARBOMER, GUAR\nHYDROXYPROPYLTRIMONIUM
        CHLORIDE, TRIDECETH-10, NIACINAMIDE, PYRUS MALUS FRUIT\nWATER / 
        APPLE FRUIT WATER, LINALOOL, PEG-100 STEARATE, STEARETH-6, 
        LIMONENE, HEXYL\nCINNAMAL, TRIDECETH-3, PHENOXYETHANOL, CITRONELLOL,
        \nFUMARIC ACID, ACETIC ACID. (F.I.L.# T70019029/1)\n5\nPat .: 
        patents.garnier.com",
        '''

        matches = self.matcher.match_allergens(ingredients)
        self.assertIn(("benzyl alcohol", "benzyl alcohol"), matches)
    
    def test_match_allergen_alternate_name(self):
        ingredients = '''
        INGREDIENTS: 1101897 FS3 AQUA / WATER / EAU, SODIUM LAURETH SULFATE, 
        GLYCOL\nDISTEARATE, SODIUM CHLORIDE, COCAMIDOPROPYL BETAINE, 
        DIMETHICONE, COCAMIDE MEA,\nPARFUM / FRAGRANCE, CITRIC ACID, 
        SODIUM BENZOATE, SODIUM HYDROXIDE, HEXYLENE\nGLYCOL, COCO-BETAINE, 
        AMODIMETHICONE, SALICYLIC ACID, CARBOMER, GUAR\nHYDROXYPROPYLTRIMONIUM
        CHLORIDE, TRIDECETH-10, NIACINAMIDE, PYRUS MALUS FRUIT\nWATER / 
        APPLE FRUIT WATER, LINALOOL, PEG-100 STEARATE, STEARETH-6, 
        LIMONENE, HEXYL\nCINNAMAL, TRIDECETH-3, PHENOXYETHANOL, CITRONELLOL,
        \nFUMARIC ACID, ACETIC ACID. (F.I.L.# T70019029/1)\n5\nPat .: 
        patents.garnier.com",
        '''

        matches = self.matcher.match_allergens(ingredients)
        self.assertGreater(len(matches), 0)
        self.assertIn(("hydroperoxides of limonene", "limonene"), matches)

    def test_match_allergens_fuzzy(self):
        ingredients = '''
        acidom benzoicum,
        INGREDIENTS: 1101897 FS3 AQUA / WATER / EAU, SODIUM LAURETH SULFATE, 
        GLYCOL\nDISTEARATE, SODIUM CHLORIDE, COCAMIDOPROPYL BETAINE, 
        DIMETHICONE, COCAMIDE MEA,\nPARFUM / FRAGRANCE, CITRIC ACID, 
        SODIUM BENZOATE, SODIUM HYDROXIDE, HEXYLENE\nGLYCOL, COCO-BETAINE, 
        AMODIMETHICONE, SALICYLIC ACID, CARBOMER, GUAR\nHYDROXYPROPYLTRIMONIUM
        CHLORIDE, TRIDECETH-10, NIACINAMIDE, PYRUS MALUS FRUIT\nWATER / 
        APPLE FRUIT WATER, LINALOOL, PEG-100 STEARATE, STEARETH-6, 
        LIMONENE, HEXYL\nCINNAMAL, TRIDECETH-3, PHENOXYETHANOL, CITRONELLOL,
        \nFUMARIC ACID, ACETIC ACID. (F.I.L.# T70019029/1)\n5\nPat .: 
        patents.garnier.com",
        '''

        matches = self.matcher.match_allergens(ingredients)
        self.assertIn(("benzoic acid", "acidum benzoicun"), matches)

    def test_fuzzy_match_single(self):
        ingredient = "acidum benzolcum"
        ingredient2 = "benz1s0nazol-2one"

        match = self.matcher.fuzzy_match_allergen(ingredient)
        self.assertEqual(match, ("benzoic acid", "acidum benzoicun"))

        match = self.matcher.fuzzy_match_allergen(ingredient2)
