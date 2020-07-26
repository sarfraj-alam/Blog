from django.shortcuts import render, HttpResponse, redirect
from . models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


#HTML Pages
def home(request):
    return render(request, 'home/home.html')



def contact(request):
    if(request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<5 or len(phone)<10 or len(content)<5:
            messages.error(request, 'Please fill the form in appropriate manner')
        else:
            contact = Contact(name = name, email = email, phone = phone, content = content)
            contact.save()
            messages.success(request, 'Your message has been sent successfully')
    return render(request, 'home/contact.html')



def about(request):
    messages.success(request, 'Welcome to the About_Us Page')
    return render(request, 'home/about.html')


def search(request):
    search = request.GET['search']
    if len(search) > 80:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=search)
        allPostsContent = Post.objects.filter(content__icontains=search)
        allPosts = allPostsTitle.union(allPostsContent)  ##union() function is used to merge the two querysets.
    if (allPosts.count() == 0):
        messages.warning(request, "No Search Results found. Please refine your query search")
    params = {'allPosts':allPosts,  'search':search}
    return render(request, 'home/search.html', params)



## Authentication API's
def handleSignup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        cpassword = request.POST['pass2']

        # check for errorneous inputs
        if len(username) > 15:
            messages.warning(request, 'Username must be in 15 characters')
            return redirect('home')
        if (password != cpassword):
            messages.warning(request, 'Passwords do not match')
            return redirect('home')
        # create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.name = name
        myuser.save()
        messages.success(request, 'Your account has been successfully created')
        return redirect('home')
    else:
        return HttpResponse('404 - Page not found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username = loginusername, password = loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
        else:
            messages.warning(request, 'Invalid username or password, please try again')
            return redirect('home')
    else:
        return HttpResponse('404 - Page not found')


def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('home')
