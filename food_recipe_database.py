from connection import mydb 
from argparse_actions import args, parser

mycursor = mydb.cursor()

def get_user(username, password):
    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = mycursor.fetchone()
    return result

def get_food(food_name, meal_category):
    mycursor.execute("SELECT * FROM foods WHERE foods_name = %s AND meal_category = %s", (food_name, meal_category))
    result = mycursor.fetchone()
    return result

def get_food_review(user_id, food_id, rating, review):
    mycursor.execute("SELECT * FROM foods_review WHERE users_id = %s AND foods_id = %s AND rating = %s AND reviews = %s", (user_id, food_id, rating, review))
    result = mycursor.fetchone()
    return result

def get_user_id(user_id):
    mycursor.execute("SELECT * FROM users WHERE id = %d", (user_id))
    result = mycursor.fetchone()
    return result

def get_food_id(food_id):
    mycursor.execute("SELECT * FROM foods WHERE id = %s", (food_id))
    result = mycursor.fetchone()
    return result

def get_food_review_id(food_review_id):
    mycursor.execute("SELECT * FROM foods_review WHERE id = %s", (food_review_id))
    result = mycursor.fetchone()
    return result

def list_user():
    mycursor.execute("SELECT id, username FROM users ORDER BY id DESC LIMIT 10")
    result = mycursor.fetchall()
    for row in result:
        print(row)

def list_food():
    mycursor.execute("SELECT id AS ID, foods_name AS Food FROM foods ORDER BY id DESC LIMIT 10")
    result = mycursor.fetchall()
    for row in result:
        print(row)

def list_food_review():
    mycursor.execute("SELECT rankingtable.Ranking, rankingtable.rating, namingtable.username, namingtable.foods_name, rankingtable.reviews "
                        "FROM "
                        "(SELECT users_id, foods_id, rating, reviews, RANK() OVER (ORDER BY rating DESC, foods_id ASC, users_id ASC) "
                        "AS Ranking "
                        "FROM foods_review) AS rankingtable "
                        "JOIN "
                        "(SELECT foods_review.users_id, foods_review.foods_id, users.username, foods.foods_name "
                        "FROM foods_review "
                        "INNER JOIN users ON foods_review.users_id = users.id "
                        "INNER JOIN foods ON foods_review.foods_id = foods.id) AS namingtable "
                        "ON rankingtable.users_id = namingtable.users_id AND rankingtable.foods_id = namingtable.foods_id ")
    result = mycursor.fetchall()
    for row in result:
        print(row)

def insert_user(username, password):
    user = get_user(username, password)
    if user:
        print(get_user(username, password))
        print("Data already exists")
        return False
    else:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        print('User', username, 'added successfully!')
        print(mycursor.rowcount, "row was inserted.")
        return True

def insert_food(food_name, meal_category):
    food = get_food(food_name, meal_category)
    if food:
        print(get_food(food_name, meal_category))
        print("Data already exists")
        return False
    else:
        sql = "INSERT INTO foods (foods_name, meal_category) VALUES (%s, %s)"
        val = (food_name, meal_category)
        mycursor.execute(sql, val)
        mydb.commit()
        print('Food item', food_name, 'added successfully!')
        print(mycursor.rowcount, "row was inserted.")
        return True

def insert_food_review(user_id, food_id, rating, review):
    food_review = get_food_review(user_id, food_id, rating, review)
    if food_review:
        print(get_food_review(user_id, food_id, rating, review))
        print("Data already exists")
        return False
    else:
        sql = "INSERT INTO foods_review (users_id, foods_id, rating, reviews) VALUES (%s, %s, %s, %s)"
        val = (user_id, food_id, rating, review)
        mycursor.execute(sql, val)
        mydb.commit()
        print('Food review and rating added successfully!')
        print(mycursor.rowcount, "row was inserted.")
        return True

if args.subcommand == 'add_user':
    username = args.username
    password = args.password
    print('Adding user', username, 'with password', password)
    insert_user(username, password)

elif args.subcommand == 'add_food':
    food_name = args.food_name
    meal_category = args.meal_category
    print('Adding food item', food_name, 'with meal category', meal_category)
    insert_food(food_name, meal_category)

elif args.subcommand == 'add_food_review':
    user_id = args.user_id
    food_id = args.food_id
    rating = args.rating
    review = args.review
    print('User', user_id, 'and Food', food_id, 'you selected')
    print('Adding food review', review, 'with rating of', rating)
    insert_food_review(user_id, food_id, rating, review)

elif args.subcommand == 'get_user':
    user_id = args.user_id
    print(type(args.user_id))
    #print(get_user_id(user_id))

elif args.subcommand == 'get_food':
    food_id = [args.food_id]
    print(get_food_id(food_id))

elif args.subcommand == 'get_food_review':
    food_review_id = [args.food_review_id]
    print(get_food_review_id(food_review_id))

elif args.subcommand == 'list_user':
    list_user()

elif args.subcommand == 'list_food':
    list_food()

elif args.subcommand == 'list_food_review':
    list_food_review()

else:
    parser.print_help()
