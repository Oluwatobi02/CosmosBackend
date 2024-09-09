from app.models.user import User
class UserService:


    @staticmethod
    def get_id_by_emails(emails):
        result = []
        for email in emails:
            user = User.objects(email=email).first()
            result.append(str(user.id))
        return result