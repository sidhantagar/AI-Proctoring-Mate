from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import auth

# Used Django's User Model to Register user.
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate,login,logout
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

# for faster mail service.
import threading

##################################PARALLEL##THREAD##FOR##MAIL############################################




# Mail thread will make mail-sending process to happen parallel to the normal page redirect.
# Added an e-mail thread.

class EmailThread(threading.Thread):

    def __init__(self,email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()




###################################REGISTER####################################################



# signUp view starts here.

def Register(request):
    user_list = []
    email_list = []

    if request.method == "POST":

        #check for username already exists!!
        for user in User.objects.values_list('username'):
            user_list.append(user[0])

        if request.POST['username'] in user_list:
            message = 'username already taken!!'
            return render(request,'signUp.html',{'name_message':message})

        #check for email already exists!!
        for mail in User.objects.values_list('email'):
            email_list.append(mail[0])

        if request.POST['email'] in email_list:
            message = 'e-mail already registered with a different user, try logging in!!'
            return render(request,'signUp.html',{'mail_message':message})
            pass

        #Check for password Validators!!
        pass_ = request.POST['pass-1']
        #validators - ['a','1'] : add instructions in .html also!
        if pass_ == request.POST['pass-2']:
            if(len(pass_) <= 6):
                message = 'Password too small!!'
                return render(request,'signUp.html',{'small_message':message})
            else:
                count_sm = 0
                count_num = 0
                for i in pass_ :
                    if(ord(i)>= 48 and ord(i)<=57):
                        count_num += 1
                    elif(ord(i)>=97 and ord(i)<=122):
                        count_sm += 1
                if(count_num == 0 or count_sm == 0):
                    message = 'Your password is weak!! - Look instructions to set a better password'
                    return render(request,'signUp.html',{'weak_message':message})
                    pass
                else:
                    #password is correct - can use it with set password!!
                    pass
        else:
            # give an error that password didn't match.
            message = "Password didn't match"
            return render(request,'signUp.html',{'pwd_message':message})
            pass

        NAME = request.POST['name'].split()
        firstName = NAME[0]
        lastName = ""
        if( len(NAME) >=2 ):
            lastName = NAME[-1]

        newUser = User.objects.create_user(username = request.POST['username'],
                    email = request.POST['email'], first_name = firstName ,
                    last_name = lastName, password = pass_)

        # work on email authentication to activate
        newUser.is_active = False
        newUser.save()
        print('POST processed!!')

        #Account Verification Using SMTP.
        current_site = get_current_site(request)
        #print(current_site.domain)
        email_subject = 'Account Activation'
        email_message = render_to_string('activate_mail_body.html',{
            'user' : newUser.first_name,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(newUser.pk)),
            'token' : generate_token.make_token(newUser)
        })

        email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [newUser.email]
        )

        EmailThread(email).start()

        #redirect it to one extra step to go!! :) page - Kindly verify your email account
        return render(request,'verification-1.html')

    return render(request,'signUp.html')





##############################LOGIN###############################################################



# Login view starts here.

def Login(request):

    if request.method == 'POST' :

        user_name = request.POST.get('user_name')
        user_pwd = request.POST.get('user_pwd')

        user = authenticate(username=user_name,password=user_pwd)
        if not user:
            #credentials that you enetered is invalid.
            text = "The Username or Password that you enetered is Invalid."
            return render(request,'logIn.html',{
                "message" : text,
                "error" : False,
            })
        else:
            if user.is_active:
                login(request,user)
                return redirect(reverse('dashboard_view'))
            else:
                text = "Please activate your account first, and then try logging in."
                return render(request,'logIn.html',{
                    "message" : text,
                    "error" : False,
                })

    return render(request,'logIn.html',{
        'message' : request.GET.get('message'),
        'error' : request.GET.get('error')
    })



##############################LOGOUT####################################################################



# Logout View starts here.

def Logout(request):

    # Everytime logout button is pressed on the page, a post request is made.
    # To this view, which redirects user, to test mate's landing page.

    if request.method == 'POST':
        logout(request)
        return redirect('home_page')



##############################SECONDARY###################################################################



# Secondary view starts here.
# Secondary view for Displaying Intermmediate Information of the site's redirect.

def Secondary(request):
    return render(request,'verification-1.html')


##############################ACCOUNT##ACTIVATE#######################################################




# Activation View starts here.
# Activation LINK sent to user's mail, will be redirected to this view

def Activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None

    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        activation_message = "Your account is successfully Activated."
        return redirect(reverse('login_page')+'?message='+activation_message+'&error=True')

    return render(request,'error-1.html')



#############################PASSWORD##RESET#########################################################################



def PasswordResetEmailForm(request):
    pass

def SetNewPassword(request,uidb64,token):
    pass

def NewPassword(request):
    pass

def PwdChangedConfirmation(request):
    pass
