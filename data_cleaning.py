import sql_administrator as sql

food_categories = []
special_diets_categories = []


def separate_types(types, food=True):
    ''' Search in every restaurant the types of food that it serves
    or special diets and separates them creating a list of categories '''

    if types.find(",") == True:
        types = types.split(",")

    if food:
        for cate in types:
            if cate not in food_categories:
                food_categories.append(cate.lower())
    else:
        for cate in types:
            if cate not in special_diets_categories:
                special_diets_categories.append(cate.lower())


def return_food_categories():
    food_categories.sort()
    return food_categories


def return_special_diets_categories():
    special_diets_categories.sort()
    return special_diets_categories


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

# sql.create_categories_tables(test_list, test_list)
# sql.populate_food_categories_table(test_tuples)
