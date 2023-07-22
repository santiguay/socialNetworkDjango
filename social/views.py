from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

''' View function to display the feed page showing all posts. '''
def feed(request):
    # Retrieve all posts from the database.
    posts = Post.objects.all()

    # Create a dictionary context containing the retrieved posts.
    context = {'posts': posts}
    
    # Render the 'feed.html' template with the context.
    return render(request, 'social/feed.html', context)

''' View function for user registration. '''
def register(request):
    # Check if the HTTP method is POST (form submission).
    if request.method == 'POST':
        # Create a UserRegisterForm instance with the POST data.
        form = UserRegisterForm(request.POST)
        # Check if the form data is valid.
        if form.is_valid():
            # Save the user object to the database.
            form.save()
            # Get the username from the form's cleaned data.
            username = form.cleaned_data['username']
            # Display a success message with the username.
            messages.success(request, f'Usuario {username} creado')
            # Redirect to the 'feed' view upon successful registration.
            return redirect('feed')
    else:
        # If the HTTP method is GET, create an empty UserRegisterForm instance.
        form = UserRegisterForm()

    # Create a dictionary context containing the UserRegisterForm instance.
    context = {'form': form}
    
    # Render the 'register.html' template with the context.
    return render(request, 'social/register.html', context)

''' View function to create a new post. '''
@login_required
def post(request):
    # Retrieve the current user from the request object.
    current_user = get_object_or_404(User, pk=request.user.pk)
    
    # Check if the HTTP method is POST (form submission).
    if request.method == 'POST':
        # Create a PostForm instance with the POST data.
        form = PostForm(request.POST)
        # Check if the form data is valid.
        if form.is_valid():
            # Save the post object to the database (without committing).
            post = form.save(commit=False)
            # Associate the post with the current user.
            post.user = current_user
            # Save the post to the database.
            post.save()
            # Display a success message for the successful post creation.
            messages.success(request, 'Post enviado')
            # Redirect to the 'feed' view upon successful post creation.
            return redirect('feed')
    else:
        # If the HTTP method is GET, create an empty PostForm instance.
        form = PostForm()
    
    # Create a dictionary context containing the PostForm instance.
    context = {'form': form}
    
    # Render the 'post.html' template with the context.
    return render(request, 'social/post.html', context)

''' View function to display the user's profile. '''
@login_required
def profile(request, username=None):
    # Retrieve the current user from the request object.
    current_user = request.user
    
    # Check if the username is provided in the URL and is different from the current user's username.
    if username and username != current_user.username:
        # If a username is provided, retrieve the user object from the database.
        user = User.objects.get(username=username)
        # Retrieve all posts associated with the user.
        posts = user.posts.all()
    else:
        # If no username provided or it matches the current user's username, use the current user.
        user = current_user
        # Retrieve all posts associated with the current user.
        posts = current_user.posts.all()
    
    # Create a dictionary context containing the user object and the associated posts.
    context = {'user': user, 'posts': posts}
    
    # Render the 'profile.html' template with the context.
    return render(request, 'social/profile.html', context)

''' View function to follow a user. '''
@login_required
def follow(request, username):
    # Retrieve the current user from the request object.
    current_user = request.user
    
    # Retrieve the user object to be followed based on the provided username.
    to_user = User.objects.get(username=username)
    # Get the ID of the 'to_user'.
    to_user_id = to_user
    # Create a new Relationship object with the current user as the 'from_user' and the target user as the 'to_user'.
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    # Save the relationship to the database.
    rel.save()
    # Display a success message indicating that the current user is now following the target user.
    messages.success(request, f'sigues a {username}')
    # Redirect to the 'feed' view after successful follow.
    return redirect('feed')

''' View function to unfollow a user. '''
def unfollow(request, username):
    # Retrieve the current user from the request object.
    current_user = request.user
    
    # Retrieve the user object to be unfollowed based on the provided username.
    to_user = User.objects.get(username=username)
    # Get the ID of the 'to_user'.
    to_user_id = to_user.id
    # Retrieve the Relationship object that represents the relationship between












