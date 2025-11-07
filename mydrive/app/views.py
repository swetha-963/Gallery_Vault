from django.shortcuts import render,redirect
from .models import *
import bcrypt
from django.core.mail import send_mail




l=[]

def loginuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            
            message = 'User not found'
            return render(request, 'login.html', {'message': message})

       
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            request.session['user'] = user.id
            message = (
                f"Hello {user.name},\n\n"
                "Thank you for joining DriVe!\n\n"
                "Best regards,\n"
                "The DriVe Team"
                    )
            
            send_mail(
               subject='sample mail',
               message=message,
               from_email='yadhuljayakumar@gmail.com',
               recipient_list=[email],
               fail_silently=False,
            )
            return redirect(home)
        else:
            message = 'Invalid credentials'
            return render(request, 'login.html', {'message': message})

    return render(request, 'login.html')

def registeruser(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        hasedpas=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        data=Users.objects.create(name=name,email=email,password=hasedpas)
        data.save()    
      

        return redirect(loginuser)                                                                

    
        
        
    return render(request,'register.html')
def home(request):
    if 'user' in request.session: 
        user=Users.objects.get(pk=request.session['user'])
        return render(request,'home.html',{'user':user})
    else:
         return redirect(loginuser)
def upload(request):
    if request.method=='POST':
        title=request.POST['title']
        file=request.FILES.get('doc')
        user=Users.objects.get(pk=request.session['user'])
        data=filess.objects.create(user=user,title=title,file=file)
        
        print(file)
        data.save()
        return redirect(home)
    return render(request,'upload.html')    
def logoutuser(request):
        del request.session['user']
        return redirect(loginuser)
def viewall(request):
    if 'user' in request.session:
        user=Users.objects.get(pk=request.session['user'])
        file=filess.objects.filter(user=user)

        print(file)

        return render(request,'view.html',{'user':user,'file':file})
    else:
        return redirect(loginuser)

