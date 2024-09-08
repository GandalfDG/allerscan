import yaml
import rapidfuzz


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
        unmatched_ingredients = ingredient_list.copy()
        for ingredient in ingredient_list:
            if ingredient in self.allergen_dict:
                matched_ingredients.append((ingredient, ingredient))
                unmatched_ingredients.remove(ingredient)
            else:
                for ingredient_name, alternate_names in self.allergen_dict.items():
                    if ingredient in alternate_names:
                        matched_ingredients.append(
                            (ingredient_name, ingredient))
                        unmatched_ingredients.remove(ingredient)

        for ingredient in unmatched_ingredients:
            fuzzy_match = self.fuzzy_match_allergen(ingredient)
            if fuzzy_match:
                matched_ingredients.append(fuzzy_match)


        return matched_ingredients

    def fuzzy_match_allergen(self, ingredient: str) -> tuple[str, str]:
        matched_results = []
        for name, alternatives in self.allergen_dict.items():
            options = list()
            options.append(name)
            options.extend(alternatives)
            result = rapidfuzz.process.extract(
                choices=options, query=ingredient, limit=1, score_cutoff=70)
            if result:
                matched_results.append((name, result[0]))

        if matched_results:
            best_match = max(matched_results, key=lambda result_tuple:
                   result_tuple[1][1])
            return (best_match[0], best_match[1][0])
        else:
            return None