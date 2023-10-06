from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from django.utils import timezone
from .forms import UserSignUpForm, LoginForm
from .models import EmailVerificationToken, User
from .email_templates import get_verification_email_body_html, get_verification_email_body_text, get_newsletter_email_body_html, get_newsletter_email_body_text
from django.contrib.auth.hashers import make_password, check_password
from decouple import config

# dummy homepage
def index(request):
    try: 
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        context = {'first_name': user.first_name}
    except:
        context = {}
    
    return render(request, 'emailModel/index.html', context)
        
# signup user
def signup(request):
    # user submits form
    if request.method == 'POST':
        signup_form = UserSignUpForm(request.POST)
        if signup_form.is_valid():

            user = signup_form.save(commit=False)
            # hashes the password and stores the hash
            user.password = make_password(user.password)
            user.save()

            # create and store verification token
            verification_token = EmailVerificationToken(user=user)
            verification_token.save()

            # send verification email
            send_verification_email(user.first_name, user.email, verification_token.token)

            return render(request, 
                  'emailModel/send_verification.html', 
                  {'first_name': user.first_name, 'email': user.email, 'token': verification_token.token, 'message': ''})
        else:
            error_message = 'User already exists or password does not match.'
    # user views form
    else:
        signup_form = UserSignUpForm()
        error_message = ''
    
    return render(request, 'emailModel/signup.html', {'form': signup_form, 'error_message': error_message})

# verify provided token and set user status to 'active'
def verify_email(request, token):
    try: 
        verification_token = EmailVerificationToken.objects.get(token=token)
        if timezone.now() > verification_token.expiration:
            return HttpResponse("Verification token has expired.")
        # set user to 'active' and delete verification token
        user = verification_token.user
        user.is_active = True
        user.save()
        verification_token.delete()
        return redirect('email:index')
    except:
        return HttpResponse("Invalid verification link or you've already verified your account.")

# logs user in
def login(request):
    
    error_message = ''
    form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # validate login form data
        if login_form.is_valid():
            # retrieve form data
            email = login_form.cleaned_data['email']
            plaintext_password = login_form.cleaned_data['password']
            print(plaintext_password)
            try:
                user = User.objects.get(email=email)
                # check password hash
                correct = check_password(plaintext_password, user.password)
                print(correct)
                if (correct):
                    if (user.is_active):
                        # remember the user
                        request.session['user_id'] = user.id
                        return redirect('email:index')
                    else:
                        error_message = 'Please verify your email before logging in.'
                else:
                    error_message = 'Password is incorrect.'
            except User.DoesNotExist:
                error_message = 'Email does not exist.'
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'error_message': error_message,
    }

    return render(request, 'emailModel/login.html', context)

# logs user out
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('email:index')

def resend_verification(request, email):
    try:
        # retrieve user name
        user = User.objects.get(email=email)
        # generate new verification token
        verification_token = EmailVerificationToken(user=user)
        verification_token.save()
        # resend verification email
        send_verification_email(user.name, email, verification_token.token)
        return render(request, 'emailModel/send_verification.html', {'first_name': user.first_name, 'email': user.email, 'token': verification_token.token, 'message': 'Another verification email was sent!'})
    except: 
        return redirect('email:index')

# move these to another module

# sends a verification email to provided email address
def send_verification_email(first_name, email, token):
    url_route = reverse('email:verify_email', args=[token])
    link = f'https://emailmodels-aaae8958e05a.herokuapp.com{url_route}' #!!!
    print(f'link: {link}')
    image_url = 'https://exitma.sfo3.cdn.digitaloceanspaces.com/static/assets/images/exitma.png'
    from_email = 'marshallxie16@gmail.com'
    to_email = email

    email_subject = f'Welcome to ExitMA, {first_name}.'
    email_body_text = get_verification_email_body_text(link)

    email_body_HTML = get_verification_email_body_html(link, image_url)

    send_mail(
        email_subject,
        email_body_text,
        from_email,
        [to_email],
        fail_silently=False,
        html_message=email_body_HTML
    )

# send mass email - should be able to send the same email to all registered members (active)
# users should not be able to see each others' emails
def send_weekly_newsletter():
    emails = []

    users = User.objects.all
    for user in users:
        recipient = user.email
        subject = 'this is some test subject line.'
        text_body = get_newsletter_email_body_text()
        html_body = get_newsletter_email_body_html()
        email = EmailMultiAlternatives(subject, text_body, 'marshallxie16@gmail.com', [recipient])
        email.attach_alternative(html_body, "text/html")
        emails.append(email)

    # Sends emails to all users
    connection = get_connection()
    connection.send_messages(emails)