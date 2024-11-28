#!/usr/bin/env python3

from re import fullmatch
import numpy as np


def get_allergen_ingredients_map(foods):
    """
    Generate a map of allergens to sets of food ingredients.
    """
    allergen_ingredients_map = {}

    for ingredients, allergens in foods:
        for allergen in allergens:

            try:
                allergen_ingredients_map[allergen].append(set(ingredients))
            except KeyError:
                allergen_ingredients_map[allergen] = [set(ingredients)]

    return allergen_ingredients_map


def get_allergen_candidates(allergen_ingredients_map):
    """
    Generate a map of allergens to candidates for the ingredient containing
    the allergen.  This is performed by looking at the intersection of
    ingredients for foods containing the allergen.  The idea is if an allergen
    is listed in two foods, it must be contained in one of the ingredients
    common to both foods.
    """
    allergen_candidates = {}

    for allergen, ingredients_sets in allergen_ingredients_map.items():
        allergen_candidates[allergen] = set.intersection(*ingredients_sets)

    return allergen_candidates


def eliminate_ingredient_candidates(allergen_candidates):
    """
    Eliminate ingredient candidates by finding an allergen with a single
    candidate ingredent and then removing that ingredient from the ingredient
    candidates of every other allergen.  Repeat until all allergens have a
    single ingredient candidate.
    """
    confirmed_allergens = {}

    while len(allergen_candidates) > 0:
        allergen, ingredient = extract_single_candidate(allergen_candidates)
        allergen_candidates.pop(allergen)
        confirmed_allergens[ingredient] = allergen

        for candidate_ingredients in allergen_candidates.values():
            candidate_ingredients -= {ingredient}

    return confirmed_allergens


def extract_single_candidate(allergen_candidates):
    """
    Extract an allergen/ingredient pair where the allergen has only a single
    candidate for ingredient.
    """
    for allergen, candidate_ingredients in allergen_candidates.items():
        if len(candidate_ingredients) == 1:
            return allergen, candidate_ingredients.pop()


def get_no_allergen_ingredients(foods, confirmed_allergens):
    """
    Find the ingredients corresponding with no allergens.
    """
    all_ingredients = []

    for ingredients, _ in foods:
        all_ingredients.extend(ingredients)

    def filter_function(ingredient):
        return ingredient not in confirmed_allergens

    return list(filter(filter_function, all_ingredients))


def get_sorted_ingredients(confirmed_allergens):
    """
    Sort the ingredients by alphabetical allergen.
    """

    def sort_function(ingredient_allergen_pair):
        _, allergen = ingredient_allergen_pair
        return allergen

    sorted_pairs = sorted(confirmed_allergens.items(), key=sort_function)
    return [ingredient for ingredient, _ in sorted_pairs]


def solve(foods):
    """
    Map each allergen to the sets of food ingredients.
    """
    allergen_ingredients_map = get_allergen_ingredients_map(foods)
    allergen_candidates = get_allergen_candidates(allergen_ingredients_map)
    confirmed_allergens = eliminate_ingredient_candidates(allergen_candidates)

    return (
        len(get_no_allergen_ingredients(foods, confirmed_allergens.keys())),
        ",".join(get_sorted_ingredients(confirmed_allergens)),
    )


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):
    foods = []

    for line in lines:
        match = fullmatch(
            "(?P<ingredients>.+) \(contains (?P<allergens>.+)\)", line.strip()
        )
        ingredients = match.group("ingredients").split()
        allergens = match.group("allergens").split(", ")
        foods.append((ingredients, allergens))

    return foods


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", (5, "mxmxvkd,sqjhc,fvjkl"))
    main("input.txt")
