import sql_administrator as sql


def separate_types(types):
    ''' Search in every restaurant the types of food that it serves
    or special diets and separates them creating a list of categories '''

    food_categories = []
    types = str(types)

    if isinstance(types, str) == False:
        types = types.split(",")

        for cate in types:
            cate = cate.strip()
            cate = cate.lower()
            cate = cate.replace(' ', '_')
            cate = cate.replace('-', '_')
            cate = cate.replace('n.a', 'n_a')

            if cate not in food_categories:
                food_categories.append(cate.lower())
    else:
        if type not in food_categories:
            food_categories.append(types)

    food_categories.sort()
    return food_categories


# x = ['a,f,h', 'a,b,d', 'c,c', 'e', 'g,g,a']
# y = ['5,1,5,5', '3,3,2', '4', '6,1,2,3,4']

# for c in x:
#     separate_types(c)

# for c in y:
#     separate_types(c, False)

# print('Letters: ', return_food_categories())
# print('Numbers: ', return_special_diets_categories())

# test_tuples = [(1, 'a,b,c,d'),
#                (2, 'c,a'),
#                (3, 'b'),
#                (4, 'a, d'),
#                (5, 'a')]

# test_list = ['a', 'b', 'c', 'd']
