import yaml


class AllergenMatcher():

    def __init__(self, allergens_yaml_path: str):
        with open(allergens_yaml_path) as infile:
            self.allergen_dict: dict[str, list[str]] = yaml.load(
                infile, Loader=yaml.SafeLoader)
        self._clean_allergen_dict()

    def _clean_allergen_dict(self):
        self.allergen_dict = {name.strip().lower():
                              [alternate.strip().lower()
                               for alternate in alternates]
                              for name, alternates in self.allergen_dict.items()}
    
    def get_allergen_dict(self):
        return self.allergen_dict

    def match_allergens(self, ingredients: str) -> list[tuple[str, str]]:
        ingredient_list: list[str] = ingredients.lower().split(",")
        ingredient_list = [ingredient.strip()
                           for ingredient in ingredient_list]

        matched_ingredients: list[tuple[str, str]] = []
        for ingredient in ingredient_list:
            if ingredient in self.allergen_dict:
                matched_ingredients.append((ingredient, ingredient))
            else:
                for ingredient_name, alternate_names in self.allergen_dict.items():
                    if ingredient in alternate_names:
                        matched_ingredients.append(
                            (ingredient_name, ingredient))
                        
        return matched_ingredients
