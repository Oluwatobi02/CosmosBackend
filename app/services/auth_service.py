from app.models.user import User, BasicInfo
from app.utils.auth_token import generate_token
class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        user = User.objects(email=email).first()
        if user:
            if user.check_password(password):
                token = generate_token(user)
                return token
        return False


    @staticmethod
    def create_user(user_info):
        try:
            basic_info = BasicInfo(**user_info.get('basic_info'))
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                basic_info=basic_info
            )
            user.set_password(user_info['password'])
            if user_info['basic_info'].get('picture'):
                print(type(user_info['basic_info'].get('picture')), 'printing type')
                user.add_picture(user_info['basic_info'].get('picture'))
            user.add_notification("Welcome to Cosmos", 'welcome')
            user.save()
            return True
        except:
            return False
        

