from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources import RegisterUser, LoginUser, ResetPassword, UserProfile, ProductManager, ProductRecommendation,BannerImageResource,BannerImageListResource,BannerImageCreateResource

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with a secure secret key
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'json']
jwt = JWTManager(app) 


# API Routes
api.add_resource(RegisterUser, '/auth/register')
api.add_resource(LoginUser, '/auth/login')
api.add_resource(ResetPassword, '/auth/password-reset')
api.add_resource(UserProfile, '/api/profile/<int:user_id>')
api.add_resource(ProductManager, '/api/products', '/api/products/<int:product_id>', '/api/products/category/<string:category>')
api.add_resource(ProductRecommendation, '/api/products/recommendations/<int:product_id>')
api.add_resource(BannerImageResource, '/images/<int:image_id>')
api.add_resource(BannerImageListResource, '/images')
api.add_resource(BannerImageCreateResource, '/images/create')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True,host='0.0.0.0')
    
#gunicorn -w 4 -b 0.0.0.0:4545 app:app --reload8u75