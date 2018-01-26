from django.shortcuts import *
from django.http import *
from .models import *
from .forms import *
from django.views.decorators.http import require_GET
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
# Create your views here.

#OR

def index(request):
    data=Post.objects.filter(Q(moderated=True)).order_by('-date_created')
    data1=Post.objects.filter(ratings__isnull=False).order_by('ratings__average')[:3]
    cat=Tag.objects.all()
    paginator = Paginator(data, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'allposts.html',{'page': page,'posts': posts,'data1':data1,'cat':cat})

def delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return HttpResponseRedirect('/post/')

def search(request):
    cat=Tag.objects.all()
    if request.method=='POST':
        squery=request.POST['search_box']
        if squery:
            data=Post.objects.filter(Q(title__icontains=squery)|Q(content__icontains=squery)|Q(user__username__exact=squery))#i=ignorecase and Q means query
            paginator = Paginator(data, 3) # 3 posts in each page
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                posts = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                posts = paginator.page(paginator.num_pages)
            if data:
                return render(request,'allposts.html',{'page': page,'posts': posts,'cat':cat})
            else:
                return render(request,'allposts.html',{'msg':'No Matching Search Result','cat':cat})
        else:
            return HttpResponseRedirect('/post/')

def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
        # List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'detail.html', {'post': post,'comments': comments,
'comment_form': comment_form})


def edit(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.date_created = timezone.now()
            post.save()
            form.save_m2m()
            form.save()
            return HttpResponseRedirect('/post/')
    else:
        form=PostForm(instance=post)
    return render(request,'edit.html',{'form':form})

def register(request):
    if request.method=='POST':
        #form=UserCreationForm(request.POST)   #built in form
        form=Regforms(request.POST)   #user created form
        #built in form usercreationform and table is user
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            profile.profilepic='pic/def.png'
            
            User.objects.create_user(username=form.cleaned_data['username'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'])
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('/login/')
    else:
        #form=UserCreationForm()
        form=Regforms()
    return render(request,'register.html',{'form':form})
@login_required
def profile(request):
    user=request.user
    if request.method=='POST':
        #form=UserCreationForm(request.POST)   #built in form
        form=MyProfile(request.POST,request.FILES)   #user created form
        #built in form usercreationform and table is user
        if form.is_valid():
            user.first_name=form.cleaned_data.get('first_name')
            user.last_name=form.cleaned_data.get('last_name')
            user.profile.location=form.cleaned_data.get('location')
            user.profile.bio=form.cleaned_data.get('bio')
            user.profile.gender=form.cleaned_data.get('gender')
            user.email=form.cleaned_data.get('email')
            user.profile.profilepic=form.cleaned_data['profilepic']
            user.profile.facebook=form.cleaned_data.get('facebook')
            user.profile.twitter=form.cleaned_data.get('twitter')
            user.profile.instagram=form.cleaned_data.get('instagram')
            user.save()
            return redirect('/post/')
    else:
        form=MyProfile(instance=user,initial={
            'location':user.profile.location,
            'gender':user.profile.gender,   
            'facebook':user.profile.facebook,
            'twitter':user.profile.twitter,
            'instagram':user.profile.instagram,
            'bio':user.profile.bio,
            'profilepic':user.profile.profilepic
            })
    return render(request,'profile.html',{'form':form})

def password(request):
    user=request.user
    if request.method=='POST':
        form =Password(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            return redirect('login')
    else:
        form=Password()
    return render(request,'password.html',{'form':form})
        

def login(request):
    return render(request,'login.html')

def auth_view(request):
    uname=request.POST['uname']
    passw=request.POST['passw']
    user=auth.authenticate(username=uname,password=passw)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/logged_in/')
    else:
        return HttpResponseRedirect('/invalid/')

def loggedin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/post/')
    else:
        return HttpResponse('Page not Found....!')

def invalid(request):
    return render(request,'invalid.html')
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
    
def post(request,tag_slug=None,category_slug=None):
    data=Post.objects.filter(Q(moderated=True)).order_by('-date_created')
    data1=Post.objects.filter(ratings__isnull=False).order_by('ratings__average')[:3]
    cat=Tag.objects.all()
    paginator = Paginator(data, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        data = data.filter(tags__in=[tag])
        paginator = Paginator(data, 3) # 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
        return render(request,'allposts.html',{'page': page,'posts': posts,'data1':data1,'tag':tag,'cat':cat})
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        data = data.filter(category=category)
        paginator = Paginator(data, 3) # 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
        return render(request,'allposts.html',{'page': page,'posts': posts,'data1':data1,'category':category,'cat':cat})
    return render(request,'allposts.html',{'page': page,'posts': posts,'data1':data1,'cat':cat})
    

@login_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.date_created = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})
@login_required
def profiledisp(request):
    return render(request,'profiledisp.html')

def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')

