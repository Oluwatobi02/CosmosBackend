from app.models.user import User
class SearchService:
    

    @staticmethod
    def populate_emails():
        users = User.objects.only('email')
        return users