from user.models import CustomUser

def generateToken(email, password):
    
    current_user = CustomUser.objects.filter(email=email)
    user = CustomUser.objects.all()
    for i in user:
        print(i.email, i.password, i.id)
    print(current_user)

