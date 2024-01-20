from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources import RegisterUser, LoginUser, ResetPassword, UserProfile, ProductManager, ProductRecommendation,BannerImageResource,BannerImageListResource,BannerImageCreateResource

app = Flask(__name__)
CORS(app)
api = Api(app)

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
    app.run(debug=False)
