from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db
from utils import generate_random_password
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import request


# class RegisterUser(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('username', required=True, help='Username cannot be blank')
#         parser.add_argument('password', required=True, help='Password cannot be blank')
#         parser.add_argument('email', required=True, help='Email cannot be blank')
#         parser.add_argument('first_name')
#         parser.add_argument('last_name')
#         data = parser.parse_args()

#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users1 WHERE username=? OR email=?", (data['username'], data['email']))
#         if cursor.fetchone():
#             return {'message': 'User with that username or email already exists'}, 400

#         hashed_password = generate_password_hash(data['password'])
#         cursor.execute("INSERT INTO users1 (username, password, email, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
#                        (data['username'], hashed_password, data['email'], data['first_name'], data['last_name']))
#         conn.commit()
#         return {'message': 'User registered successfully'}, 201


class RegisterUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Username cannot be blank')
        parser.add_argument('password', required=True, help='Password cannot be blank')
        parser.add_argument('email', required=True, help='Email cannot be blank')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('profile_picture')  # Added profile_picture field
        data = parser.parse_args()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users1 WHERE username=? OR email=?", (data['username'], data['email']))
        
        if cursor.fetchone():
            return {'message': 'User with that username or email already exists'}, 400

        hashed_password = generate_password_hash(data['password'])
        cursor.execute("INSERT INTO users1 (username, password, email, first_name, last_name, profile_picture) VALUES (?, ?, ?, ?, ?, ?)",
                       (data['username'], hashed_password, data['email'], data['first_name'], data['last_name'], data['profile_picture']))
        conn.commit()

        # Retrieve the newly registered user for response
        cursor.execute("SELECT * FROM users1 WHERE username=?", (data['username'],))
        new_user = cursor.fetchone()

        user_details = {
            'id': new_user['id'],
            'username': new_user['username'],
            'email': new_user['email'],
            'first_name': new_user['first_name'],
            'last_name': new_user['last_name'],
            'profile_picture': new_user['profile_picture'],
            'has_profile_picture': new_user['has_profile_picture']
        }

        return {'message': 'User registered successfully', 'user_details': user_details}, 201

# class LoginUser(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('username', required=True, help='Username cannot be blank')
#         parser.add_argument('password', required=True, help='Password cannot be blank')
#         data = parser.parse_args()

#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users1 WHERE username=?", (data['username'],))
#         user = cursor.fetchone()

#         if user and check_password_hash(user['password'], data['password']):
#             return {'message': 'Login successful'}, 200
#         else:
#             return {'message': 'Invalid credentials'}, 401
    
class LoginUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Username cannot be blank')
        parser.add_argument('password', required=True, help='Password cannot be blank')
        data = parser.parse_args()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users1 WHERE username=?", (data['username'],))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], data['password']):
            user_details = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'profile_picture': user['profile_picture'],
                'has_profile_picture': user['has_profile_picture']
            }
            return {'message': 'Login successful', 'user_details': user_details}, 200
        else:
            return {'message': 'Invalid credentials'}, 401


class ResetPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email cannot be blank')
        data = parser.parse_args()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users1 WHERE email=?", (data['email'],))
        user = cursor.fetchone()

        if user:
            new_password = generate_random_password()
            hashed_password = generate_password_hash(new_password)
            cursor.execute("UPDATE users1 SET password=? WHERE email=?", (hashed_password, data['email']))
            conn.commit()
            # Ideally, send new password via email or other secure method
            return {'message': 'Password reset successful. New password has been sent.'}, 200
        else:
            return {'message': 'User with that email does not exist'}, 404

class UserProfile(Resource):
    def get(self, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users1 WHERE id=?", (user_id,))
        user = cursor.fetchone()

        if user:
            profile_data = {
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'profile_picture': user['profile_picture'],
                'has_profile_picture': user['has_profile_picture']
            }
            return profile_data, 200
        else:
            return {'message': 'User not found'}, 404

    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('profile_picture')
        parser.add_argument('has_profile_picture', type=int)
        data = parser.parse_args()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users1 SET first_name=?, last_name=?, profile_picture=?, has_profile_picture=? WHERE id=?",
                       (data['first_name'], data['last_name'], data['profile_picture'], data['has_profile_picture'], user_id))
        conn.commit()
        return {'message': 'User profile updated successfully'}, 200

# class ProductManager(Resource):
#     def get(self, product_id=None, category=None):
#         conn = get_db()
#         cursor = conn.cursor()
#         if product_id is not None:
#             cursor.execute("SELECT * FROM Products WHERE id=?", (product_id,))
#         elif category is not None:
#             cursor.execute("SELECT * FROM Products WHERE category=?", (category,))
#         else:
#             cursor.execute("SELECT * FROM Products")

#         rows = cursor.fetchall()
#         if not rows:
#             return {'message': 'No products found'}, 404

#         products = [dict(row) for row in rows]
#         return {'products': products}, 200
    
class ProductManager(Resource):
    def get(self, product_id=None, category=None):
        conn = get_db()
        cursor = conn.cursor()
        if product_id is not None:
            cursor.execute("SELECT * FROM Products WHERE id=?", (product_id,))
        elif category is not None:
            cursor.execute("SELECT * FROM Products WHERE category=?", (category,))
        else:
            cursor.execute("SELECT * FROM Products")

        rows = cursor.fetchall()
        if not rows:
            return {'message': 'No products found'}, 404

        products = [dict(row) for row in rows]
        return {'products': products}, 200


class ProductRecommendation(Resource):
    def get(self, product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products WHERE id=?", (product_id,))
        target_product = cursor.fetchone()

        if not target_product:
            return {'message': 'Product not found'}, 404

        # Fetch all products including their specifications, names, IDs, and images
        cursor.execute("SELECT id, name, specifications, image_links FROM Products")
        all_products = cursor.fetchall()

        # Building TF-IDF matrix
        vectorizer = TfidfVectorizer()
        descriptions = [product['specifications'] for product in all_products]
        tfidf_matrix = vectorizer.fit_transform(descriptions)

        # Finding the index of the target product
        target_index = next(index for index, product in enumerate(all_products) if product['id'] == product_id)

        # Compute cosine similarity
        cosine_similarities = cosine_similarity(tfidf_matrix[target_index], tfidf_matrix).flatten()
        similar_indices = np.argsort(-cosine_similarities)[1:6]  # Get indices of top 5 similar products

        # Fetch similar products with their details
        similar_products = []
        for i in similar_indices:
            similar_product = all_products[i]
            similar_products.append({
                'id': similar_product['id'],
                'name': similar_product['name'],
                'image_links': similar_product['image_links']
            })

        return {'similar_products': similar_products}, 200


def requires_login(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Authorization header is missing'}, 401

        # Assuming you have a function to verify the token and get user information
        user_info = verify_token(auth_header)
        if not user_info or not check_password_hash(user_info['password_hash'], user_info['password']):
            return {'message': 'Invalid authentication credentials'}, 401

        # Attach the user information to the global context 'g' for later use
        g.user = user_info

        return func(*args, **kwargs)

    return wrapper


class BannerImageResource(Resource):
    def get(self, image_id):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM BannerImages WHERE id = ?", (image_id,))
        image = cursor.fetchone()

        conn.close()

        if image:
            return {'id': image['id'], 'name': image['name'], 'image': image['image'], 'status': image['status']}
        else:
            return {'message': 'Image not found'}, 404

    def put(self, image_id):
        conn = get_db()
        cursor = conn.cursor()

        data = request.get_json()
        name = data['name']
        image = data['image']
        status = data.get('status', 1)  # Default to active if not provided

        cursor.execute("UPDATE BannerImages SET name=?, image=?, status=? WHERE id=?",
                       (name, image, status, image_id))
        conn.commit()
        conn.close()

        return {'message': 'Image updated successfully'}

    def delete(self, image_id):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM BannerImages WHERE id=?", (image_id,))
        conn.commit()
        conn.close()

        return {'message': 'Image deleted successfully'}

class BannerImageListResource(Resource):
    def get(self):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM BannerImages WHERE status = 1")
        images = cursor.fetchall()

        conn.close()

        return [{'id': image['id'], 'name': image['name'], 'image': image['image'], 'status': image['status']}
                for image in images]

class BannerImageCreateResource(Resource):
    def post(self):
        conn = get_db()
        cursor = conn.cursor()

        data = request.get_json()
        name = data['name']
        image = data['image']
        status = data.get('status', 1)  # Default to active if not provided

        cursor.execute("INSERT INTO BannerImages (name, image, status) VALUES (?, ?, ?)",
                       (name, image, status))
        conn.commit()
        conn.close()

        return {'message': 'Image created successfully'}, 201