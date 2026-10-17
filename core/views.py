from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth import login, logout, authenticate # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.models import User # type: ignore
from core.models import Post, Comment, Profile # type: ignore

# --- 1. OFFLINE TRANSLATION ENGINE MATRIX ---
TRANSLATIONS = {
    'en': {
        'brand': 'ConnectHub', 'home': 'Home', 'users': 'Users', 'profile': 'Profile', 'logout': 'Logout',
        'feed_title': 'Your Feed', 'create_btn': '+ Create New Post', 'placeholder': "What's on your mind?",
        'publish': 'Publish Post', 'cancel': 'Cancel', 'empty': 'Your timeline feed is empty.',
        'like': 'Like', 'liked': 'Liked', 'comments': 'Comments', 'send': 'Send',
        'write_comment': 'Write a comment...', 'discover': 'Discover Members', 'followers': 'Followers',
        'following': 'Following', 'posts': 'Posts', 'view_profile': 'View Profile', 'follow': 'Follow',
        'unfollow': 'Unfollow', 'edit_profile': 'Edit Basic Profile', 'save_bio': 'Save Bio', 'delete': 'Delete'
    },
    'ta': {
        'brand': 'கனெக்ட்ஹப்', 'home': 'முகப்பு', 'users': 'பயனர்கள்', 'profile': 'சுயவிவரம்', 'logout': 'வெளியேறு',
        'feed_title': 'உங்கள் பதிவுவரிசை', 'create_btn': '+ புதிய பதிவு', 'placeholder': 'உங்கள் மனதில் என்ன தோன்றுகிறது?',
        'publish': 'பதிவிடு', 'cancel': 'ரத்துசெய்', 'empty': 'உங்கள் பதிவுவரிசை காலியாக உள்ளது.',
        'like': 'விருப்பு', 'liked': 'விருப்பம் தெரிவிக்கப்பட்டது', 'comments': 'கருத்துகள்', 'send': 'அனுப்பு',
        'write_comment': 'உங்கள் கருத்தை எழுதுங்கள்...', 'discover': 'உறுப்பினர்களைக் கண்டறியவும்', 'followers': 'பின்தொடர்பவர்கள்',
        'following': 'பின்தொடர்வது', 'posts': 'பதிவுகள்', 'view_profile': 'சுயவிவரம் பார்', 'follow': 'பின்தொடர்',
        'unfollow': 'விலகு', 'edit_profile': 'சுயவிவரத்தை மாற்று', 'save_bio': 'பயோ சேமி', 'delete': 'நீக்கு'
    }
}

def get_language_context(request):
    """Fetches dictionary maps based on user choice state saved inside session data cache"""
    active_lang = request.session.get('platform_lang', 'en')
    return {
        'lang': TRANSLATIONS[active_lang],
        'current_lang': active_lang
    }

def set_language_view(request):
    """Captures selector values submitted via the template navbar form stream"""
    if request.method == 'POST':
        selected_lang = request.POST.get('language_selection', 'en')
        request.session['platform_lang'] = selected_lang
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# --- 2. AUTHENTICATION VIEWS ---
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# --- 3. TIMELINE FEED CONTROLLERS ---
@login_required
def home_view(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    context.update(get_language_context(request))
    return render(request, 'core/home.html', context)

@login_required
def create_post_view(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image_file = request.FILES.get('image')
        video_file = request.FILES.get('video')
        
        if content or image_file or video_file:
            Post.objects.create(
                user=request.user, 
                content=content,
                image=image_file,
                video=video_file
            )
            return redirect('home')
            
    context = {}
    context.update(get_language_context(request))
    return render(request, 'core/create_post.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# --- 4. SOCIAL MATRIX ACTION TRACKING ---
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# --- 5. MEMBER DIRECTORY PROFILE VIEW RESOLUTIONS ---
@login_required
def users_view(request):
    profiles = Profile.objects.exclude(user=request.user)
    context = {'profiles': profiles}
    context.update(get_language_context(request))
    return render(request, 'core/users.html', context)

@login_required
def profile_view(request, username=None):
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user
        
    profile, created = Profile.objects.get_or_create(user=user_obj)
    user_posts = Post.objects.filter(user=user_obj)
    
    if request.method == 'POST' and request.user == user_obj:
        bio = request.POST.get('bio', '').strip()
        profile.bio = bio
        profile.save()
        return redirect('profile', username=user_obj.username)
        
    context = {'profile': profile, 'posts': user_posts, 'user_obj': user_obj}
    context.update(get_language_context(request))
    return render(request, 'core/profile.html', context)

@login_required
def toggle_follow(request, profile_id):
    target_profile = get_object_or_404(Profile, id=profile_id)
    user_profile = request.user.profile
    
    if target_profile in user_profile.following.all():
        user_profile.following.remove(target_profile)
    else:
        user_profile.following.add(target_profile)
    return redirect(request.META.get('HTTP_REFERER', 'users'))
