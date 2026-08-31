from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Story, Node, Choice, UserAccount, Rating, Bookmark, PlaySession, Comment, Profile
from .forms import SignUpForm, SignInForm, CommentForm, ProfileForm, UserEditForm

def homepage(request):
    stories = Story.objects.filter(is_published=True).order_by('-created_at')[:10]
    return render(request, 'stories/homepage.html', {'stories': stories})

def search_view(request):
    query = request.GET.get('q', '')
    stories = Story.objects.filter(is_published=True, title__icontains=query) if query else []
    return render(request, 'stories/search.html', {'stories': stories, 'query': query})

def leaderboard(request):
    stories = Story.objects.filter(is_published=True).order_by('-play_count')[:20]
    return render(request, 'stories/leaderboard.html', {'stories': stories})

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    comments = story.comments.all()
    form = CommentForm()
    return render(request, 'stories/story_detail.html', {'story': story, 'comments': comments, 'form': form})

def story_play(request, story_id, node_id=None):
    story = get_object_or_404(Story, id=story_id)
    
    if node_id:
        node = get_object_or_404(Node, id=node_id, story=story)
    else:
        node = story.start_node
        if not node:
            node = story.nodes.first()
            
    if not node:
        return render(request, 'stories/error.html', {'message': "Story has no nodes."})
        
    if node.is_ending:
        return render(request, 'stories/_ending.html', {'story': story, 'node': node})
        
    return render(request, 'stories/story_play.html', {'story': story, 'node': node})

def story_choose(request, story_id):
    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        choice = get_object_or_404(Choice, id=choice_id)
        if choice.next_node:
            return redirect('story_play_node', story_id=story_id, node_id=choice.next_node.id)
        else:
            # Here is where the AI logic goes later
            return redirect('story_play', story_id=story_id)
    return redirect('story_detail', story_id=story_id)

def story_restart(request, story_id):
    return redirect('story_play', story_id=story_id)

@login_required
def bookmark_toggle(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, story=story)
    if not created:
        bookmark.delete()
    return redirect('story_detail', story_id=story_id)

@login_required
def rate_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    stars = int(request.POST.get('stars', 0))
    if 1 <= stars <= 5:
        Rating.objects.update_or_create(user=request.user, story=story, defaults={'stars': stars})
    return redirect('story_detail', story_id=story_id)

@login_required
def add_comment(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.story = story
            comment.save()
    return redirect('story_detail', story_id=story_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    story_id = comment.story.id
    if request.method == 'POST':
        comment.delete()
    return redirect('story_detail', story_id=story_id)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user)
            UserAccount.objects.create(user=user, username=username, hashed_password=user.password)
            login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'stories/signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('homepage')
            else:
                form.add_error(None, 'Invalid credentials.')
    else:
        form = SignInForm()
    return render(request, 'stories/signin.html', {'form': form})

def signout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def profile_view(request):
    return render(request, 'stories/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'stories/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})