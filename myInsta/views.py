from django.shortcuts import render,redirect,HttpResponse
from .models import Profile,Post,Follow,Likes,Comments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
@login_required(login_url='/accounts/login')
def mainPage(request):
    user = request.user
    try:
        tot_following_list = Follow.objects.get(curr_user=user).followed.all()
        tot_following_list = list(tot_following_list)
        tot_following_list.append(user)
        all_user_posts = Post.objects.filter(curr_user__in = tot_following_list).order_by('-pk')
        post_liked = []
        for i in all_user_posts:
            is_liked = Likes.objects.filter(curr_user = user, post=i)
            if is_liked:
                post_liked.append(i)
        return render(request,'main_page.html',{'user_posts':all_user_posts,'liked_post':post_liked})
    except:
        print("helll")
        return render(request,'main_page1.html',{'user':user})

@login_required(login_url='/accounts/login')
def profile_page(request):
    user = request.user
    ProfilePicture = Profile.objects.get(curr_user=user)
    user_profile_pic =  ProfilePicture.profile_pic
    user_bio = ProfilePicture.user_bio
    user_posts = Post.objects.filter(curr_user=user)
    try:
        tot_following_list = Follow.objects.get(curr_user=user).followed.all()
        tot_followers_list = Follow.objects.filter(followed=user)
        tot_no_following = tot_following_list.count()
        tot_no_followers = tot_followers_list.count()
    except:
        tot_no_following = '0'
        tot_no_followers = '0'
    return render(request,'profile.html',context={'user':user,'profilePic':user_profile_pic,'userbio':user_bio,'user_posts':user_posts,'no_of_following':tot_no_following,'no_of_posts':user_posts.count(),'no_of_followers':tot_no_followers})


@login_required(login_url='/accounts/login')
def UpdateProfile(request,UID):
    user = request.user
    if request.method == 'POST':
        profile_pic_new = request.POST.get('imageHidden')
        updatedUserName = request.POST.get('updated_username')
        updatedFirstName = request.POST.get('updated_fname')
        updatedLastName = request.POST.get('updated_lname')
        userBio = request.POST.get('bio')
        current_user = User.objects.get(id=UID)
        current_user.username = updatedUserName
        current_user.first_name = updatedFirstName
        current_user.last_name = updatedLastName
        current_user.save()
        new_profile_pic = Profile.objects.get(curr_user=current_user)
        new_profile_pic.profile_pic = profile_pic_new
        new_profile_pic.user_bio = userBio
        new_profile_pic.save()
        return redirect(profile_page)
    else:
        ProfilePicture = Profile.objects.get(id=UID)
        userid = ProfilePicture.curr_user.id
        user = User.objects.get(id=userid)
        user_profile_pic =  ProfilePicture.profile_pic
        user_bio = ProfilePicture.user_bio
        user_posts = Post.objects.filter(curr_user=user)
        is_following = Follow.objects.filter(curr_user=request.user,followed=user)
        try:
            tot_following_list = Follow.objects.get(curr_user=user).followed.all()
            tot_followers_list = Follow.objects.filter(followed=user)
            tot_no_following = tot_following_list.count()
            tot_no_followers = tot_followers_list.count()
        except:
            tot_no_following = '0'
            tot_no_followers = '0'
        return render(request,'profile.html',context={'user':user,'profilePic':user_profile_pic,'userbio':user_bio,'user_posts':user_posts,'connection':is_following,'no_of_following':tot_no_following,'no_of_posts':user_posts.count(),'no_of_followers':tot_no_followers})

@login_required(login_url='/accounts/login')
def post_page(request):
    user = request.user
    if request.method == 'POST':
        post_image = request.POST.get('imageHidden')
        post_caption = request.POST.get('caption')
        user_profile = Profile.objects.get(curr_user=user)
        user_post = Post(curr_user=user,curr_profile=user_profile,post_image=post_image,post_caption=post_caption)
        user_post.save()
        return redirect(mainPage)
    else:
        return render(request,'upload_post.html')


@login_required(login_url='/accounts/login')
def explore(request):
    user = request.user
    users = User.objects.all()
    all_users = []
    all_profiles = []
    for i in users:
        if i.is_superuser == False and i!=user:
            all_profiles.append(Profile.objects.get(curr_user=i))
            all_users.append(i)
    return render(request,'explore.html',{'all_users':all_users,'all_profiles':all_profiles})
@login_required(login_url='/accounts/login')
def follow(request,UID):
    user = request.user
    another_user = User.objects.get(id=UID)
    # check if already following
    following = Follow.objects.filter(curr_user=user,followed=another_user)
    is_following = True if following else False

    if is_following:
        Follow.unfollow(user,another_user)
        is_following = False
    else:
        Follow.follow(user,another_user)
        is_following = True
    pid = Profile.objects.get(curr_user=another_user)  
  
    resp = {
        'following' : is_following,
    }
    response = json.dumps(resp)
    return HttpResponse(response,content_type = "application/json")

@login_required(login_url='/accounts/login')
def liked(request):
    user = request.user
    pid = request.GET.get('liked_id','')
    liked_post = Post.objects.get(id=pid)
    like = Likes.objects.filter(curr_user=user,post=liked_post)
    liked = True if like else False
    if liked:
        Likes.user_disliked(liked_post,user)
        liked = False
    else:
        Likes.user_liked(liked_post,user)
        liked = True

    like_count = Likes.objects.get(post=liked_post)
    like_count = like_count.post.post_likes
    resp = {
        'liked' : liked,
        'like_count' : like_count,
    }
    response = json.dumps(resp)
    return HttpResponse(response,content_type = "application/json")
 
@login_required(login_url='/accounts/login')
def comments_section(request):
    user = request.user
    comments = request.GET.get('inputValue','')
    PID = request.GET.get('postId')
    post = Post.objects.get(id=int(PID))
    comment_obj = Comments(curr_user=user,curr_post=post)
    comment_obj.comment = comments
    comment_obj.save()
    return redirect(mainPage)
    
@login_required(login_url='/accounts/login')
def delPost(request,PID):
    post = Post.objects.get(id=PID)
    post.delete()
    return redirect(mainPage)






