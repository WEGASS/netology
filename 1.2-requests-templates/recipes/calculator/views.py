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


def get_recipe(request, recipe):
    quantity = int(request.GET.get('servings', 1))
    final_recipe = {}
    if recipe in DATA.keys():
        for name, value in DATA[recipe].items():
            final_recipe[name] = value * quantity
    context = {
        'recipe': final_recipe
    }
    return render(request, 'calculator/index.html', context)


