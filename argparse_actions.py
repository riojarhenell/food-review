from connection import mydb 
import argparse

"""
unstaged changes
"""

mycursor = mydb.cursor()

parser = argparse.ArgumentParser(prog='Food Recipes CLI',
                                description='Food Recipes CLI',
                                epilog='Thank you!')

subparsers = parser.add_subparsers(title='subcommands', dest='subcommand', required=False, help='sub-command help')

add_user_parser = subparsers.add_parser('add_user', help='To add user')
add_user_parser.add_argument('--username', '-u', type=str, help="Please input your username")
add_user_parser.add_argument('--password', '-p', type=str, help="Please input your password")

add_food_parser = subparsers.add_parser('add_food', help='To add food')
add_food_parser.add_argument('--food_name', '-f', type=str, help="Please input your food name")
add_food_parser.add_argument('--meal_category', '-mc', type=str, help="Please input your food meal category")

add_food_review_parser = subparsers.add_parser('add_food_review', help="To add food review" )
add_food_review_parser.add_argument('--user_id', '-ud', type=int, help="Please input your user id")
add_food_review_parser.add_argument('--food_id', '-fd', type=int, help="Please input your food id")
add_food_review_parser.add_argument('--rating', '-rt', type=int, help="Please input your rating")
add_food_review_parser.add_argument('--review', '-rw', type=str, help="Please input your review")

get_user_parser = subparsers.add_parser('get_user', help='To get user')
get_user_parser.add_argument('--user_id', '-gud', type=int, help="Please input a valid user id")

get_food_parser = subparsers.add_parser('get_food', help='To add food')
get_food_parser.add_argument('--food_id', '-gfd', type=int, help="Please input a valid food id")

get_food_review_parser = subparsers.add_parser('get_food_review', help="To get food review" )
get_food_review_parser.add_argument('--food_review_id', '-gfrd', type=int, help="Please input a valid food review id")

list_user_parser = subparsers.add_parser('list_user', help='To list 10 latest user')

list_food_parser = subparsers.add_parser('list_food', help='To list 10 latest food')

list_food_review_parser = subparsers.add_parser('list_food_review', help="To list top 10 foods based on rating" )

args = parser.parse_args()