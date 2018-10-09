from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, PostImage, Prof, CommentForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from .models import Image, Profile


# Create your views here.
@login_required
def index(request):
    images = Image.objects.all()
    comnt = CommentForm()
    return render(request, 'index.html', {"images":images,"comnt":comnt})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile(user=user)
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your picity account.'
            message = render_to_string('activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can' '<a href="/accounts/login"> login </a>your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def profile(request):

    current_user = request.user
    form = PostImage()
    images=Image.objects.filter(user=current_user)
    profile = Prof()
    if request.method == 'POST':
        form = PostImage(request.POST, request.FILES)
        profile = Prof(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        elif profile.is_valid():
            prf = profile.save(commit=False)
            prf.user = current_user
            prf.save()
    return render(request,'profile.html', {"form":form, 'images':images, 'profile':profile})


@login_required()
def new_post(request):

        return redirect('index')


def comment(request,id):
    post=Image.objects.get(id=id)
    if request.method == 'POST':
        comnt=CommentForm(request.POST)
        if comnt.is_valid():
            comment=comnt.save(commit=False)
            comment.user=request.user
            comment.image=post
            comment.save()
            return redirect('index')
    return redirect('index')


def search_user(request):
    if 'user' in request.GET or request.GET['user']:
        search_item = request.GET.get('user')
        searched_users = User.objects.filter(username__icontains=search_item)
        message = f"{search_item}"
        return render(request,'search.html',{"message":message,"users":searched_users})
    else:
        message = "You have not searched for any users yet"
        return render(request, 'search.html',{"message":message})