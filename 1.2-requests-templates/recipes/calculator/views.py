from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def recipe_view(request, dish_name):
    # Получаем рецепт из DATA
    recipe = DATA.get(dish_name)

    if not recipe:
        return HttpResponse(f'Рецепт "{dish_name}" не найден', status=404)

    # Получаем параметр servings (по умолчанию 1)
    servings = request.GET.get('servings')

    if servings is not None:
        try:
            servings = int(servings)
            if servings < 1:
                servings = 1
        except ValueError:
            servings = 1
    else:
        servings = 1

    # Умножаем количество ингредиентов на число порций
    scaled_recipe = {}
    for ingredient, amount in recipe.items():
        scaled_recipe[ingredient] = amount * servings

    context = {
        'recipe': scaled_recipe,
        'dish_name': dish_name,
        'servings': servings,
    }

    return render(request, 'calculator/recipe.html', context)
def home_view(request):
    return render(request, 'calculator/home.html', {'recipes': DATA.keys()})