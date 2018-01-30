from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from twitter.form import SignUpForm, TweetForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile, Tweets

# Create your views here.


def signup(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.profile_image = form.cleaned_data.get('profile_image')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(user)
            login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()
        context = {'form': form}

    return render(request, 'twitter/signup.html', context)


@login_required
def home(request):
    form_tweet = TweetForm()
    context = {}
    if request.method == 'POST':
        return redirect('home')
    else:
        form = SignUpForm()
        profile = Profile.objects.get(user=request.user)
        print(profile.profile_image.url)
        follow_user = profile.followers.all()
        id_list = []
        for usr in follow_user:
            if usr.id != request.user.id:
                id_list.append(usr.id)


        user_list = User.objects.exclude(pk__in=id_list)
        # get tweets
        exc_user = []
        for u in user_list:
            if u.id != request.user.pk:
                exc_user.append(u.id)
        tweets = Tweets.objects.exclude(created_by__in=exc_user).order_by('created_date')
        context = {'form': form, 'form_tweet': form_tweet, 'user_list': user_list, 'follow_user': follow_user,
                   'tweets': tweets}

    return render(request, 'twitter/home.html', context)


@login_required
def follower(request):
    if request.method == 'GET':
        user_id = request.GET['post_id']
        follower_user = User.objects.get(pk=int(user_id))
        user = User.objects.get(pk=request.user.pk)
        profile = get_object_or_404(Profile, user=user)
        profile.followers.add(follower_user)
        profile.save()
        user.save()
        return HttpResponse("Success!") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")

@login_required
def unfollower(request):
    print("inside unfollow")
    if request.method == 'GET':
        user_id = request.GET['unfollow_id']
        unfollower_user = User.objects.get(pk=int(user_id))
        user = User.objects.get(pk=request.user.pk)
        profile = get_object_or_404(Profile, user=user)
        profile.followers.remove(unfollower_user)
        profile.save()
        user.save()
        return HttpResponse("Success!") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")




@login_required
def add_tweet(request):
    if request.method =='POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.created_by = request.user
            tweet.save()
            return redirect('home')
    else:
        return redirect('home')
