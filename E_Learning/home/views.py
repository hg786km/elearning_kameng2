from django.shortcuts import render,redirect
import pyrebase
from django.contrib import auth
from functions import *
from decorators import *


config = {
    "apiKey": "AIzaSyAEue4ktaLv-1wqKQgtgkfWJ1Oj6NNW-8U",
    "authDomain": "e-learning-ccbd8.firebaseapp.com",
    "databaseURL": "https://e-learning-ccbd8.firebaseio.com",
    "projectId": "e-learning-ccbd8",
    "storageBucket": "e-learning-ccbd8.appspot.com",
    "messagingSenderId": "1053587965345",
    "appId": "1:1053587965345:web:b97bb311c911183b0d77e0",
    "measurementId": "G-K1YGG2H5VQ"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required

def add_notes(request):
    if request.method == 'GET':
        return render(request, "home/add_notes.html")

    else:
        notes_name = request.POST.get('notes_name')
        url = request.POST.get('url')
        upload = request.FILES.get('url')
        print(upload)
        try:
            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId']
            # a contains local id
        except:
            return render(request, "accounts/login.html")

        storage = firebase.storage()

        storage_path = "notes/" + notes_name + ".pdf"
        print(storage_path)
        storage.child(storage_path).put(upload, idtoken)
        url = storage.child(storage_path).get_url(idtoken)

        username = database.child("users").child(a).child("details").child("username").get(idtoken).val()
        tags = database.child("users").child(a).child("details").child("admin").get(idtoken).val()

        # print(username)
        data = {
            "tags": tags,
            "url": url,
            "username": username,
            "approved": 0,
        }

        database.child('Notes').child(notes_name).set(data, idtoken)
        return render(request, "home/notes.html")


@login_required
def view_notes(request):
    notes = database.child('Notes').shallow().get().val()
    print(notes)
    list_notes = [*notes]
    print(list_notes)
    tags = []
    urls = []
    usernames = []
    approved = []
    for i in list_notes:
        tag = database.child('Notes').child(i).child('tags').get().val()
        tags.append(tag)
        url = database.child('Notes').child(i).child('url').get().val()
        urls.append(url)
        username = database.child('Notes').child(i).child('username').get().val()
        usernames.append(username)
        approve = database.child('Notes').child(i).child('approved').get().val()
        approved.append(approve)

    print(tags)
    print(urls)
    print(usernames)
    combine_list = zip(list_notes,tags,usernames,urls,approved)
    return render(request, "home/display_notes.html", {'combine_list':combine_list})

@login_required
def add_club(request):
        if request.method == 'GET':
            return render(request, "home/add_club.html")

        else:
            print("falak")
            url = request.POST.get('url')
            print(url)
            upload = request.FILES.get('url')
            print(upload)

            try:
                idtoken = request.session['uid']
                a = authe.get_account_info(idtoken)
                a = a['users']
                a = a[0]
                a = a['localId']
                # a contains local id
            except:
                return render(request, "accounts/login.html")

            storage = firebase.storage()

            storage_path = "clubs/" + tags
            storage.child(storage_path).put(upload, idtoken)
            url = storage.child(storage_path).get_url(idtoken)

            username = database.child("users").child(a).child("details").child("username").get(idtoken).val()
            tags = database.child("users").child(a).child("details").child("admin").get(idtoken).val()
            # print(username)
            data = {
                "url": url,
                "username": username,
                "approved": 0,
            }

            database.child('Clubs').child(tags).set(data, idtoken)
            return render(request, "home/homepage.html")
@login_required
def display_clubs(request):
    clubs = database.child('Clubs').shallow().get().val()
    print(clubs)
    list_clubs = [*clubs]
    print(list_clubs)
    urls = []
    usernames = []
    approved = []
    for i in list_clubs:
        url = database.child('Notes').child(i).child('url').get().val()
        urls.append(url)
        username = database.child('Notes').child(i).child('username').get().val()
        usernames.append(username)
        approve = database.child('Notes').child(i).child('approved').get().val()
        approved.append(approve)

    print(urls)
    print(usernames)
    combine_list = zip(list_clubs,usernames,urls,approved)
    return render(request, "home/display_clubs.html", {'combine_list':combine_list})
@login_required
def addbook(request):
    if request.method =='GET':
        return render(request,"home/addbook.html")
    else:
        bookname=request.POST.get('book_name')
        url = request.POST.get('url')
        upload = request.FILES.get('url')


        try:
            idtoken=request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users']
            a=a[0]
            a=a['localId']
        except:
            return render(request,"accounts/signup.html")

        storage = firebase.storage()
        storage_path = "books/" + bookname + ".pdf"
        storage.child(storage_path).put(upload, idtoken)
        url = storage.child(storage_path).get_url(idtoken)

        username = database.child("users").child(a).child("details").child("username").get(idtoken).val()
        email = database.child("users").child(a).child("details").child("email").get(idtoken).val()
        tags = database.child("users").child(a).child("details").child("admin").get(idtoken).val()
        print(tags)
        data={
            "tags":tags,
            "username":username,
            "status": 1,
            "email": email,
            "url": url,
            "approved": 0,
        }
        database.child("books").child(bookname).set(data,idtoken)
        return render(request,"home/books.html")


@login_required

def displaybook(request):
    books = database.child('books').shallow().get().val()

    list_books = [*books]

    tags = []
    usernames = []
    status = []
    emails = []
    approved = []
    urls = []
    for i in list_books:
        tag = database.child('books').child(i).child('tags').get().val()
        tags.append(tag)
        username = database.child('books').child(i).child('username').get().val()
        usernames.append(username)
        email = database.child('books').child(i).child('email').get().val()
        emails.append(email)
        url = database.child('books').child(i).child('url').get().val()
        urls.append(url)
        statusz = database.child('books').child(i).child('status').get().val()
        status.append(statusz)
        approve = database.child('books').child(i).child('approved').get().val()
        approved.append(approve)

    print(approved)
    combine_list = zip(list_books,tags,usernames,status,emails,approved,urls)
    return render(request, "home/display_books.html", {'combine_list':combine_list})


j=1


@login_required
def requestbook(request,username,book_title,status):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
    except:
        return render(request, "accounts/signup.html")


    req_user = database.child("users").child(a).child("details").child("username").get(idtoken).val()
    data = {
        "owner": username,
        "req_user": req_user,
        "status":status,
        "book_title":book_title,
    }
    global j
    j = j + 1
    database.child("requests").child(j).set(data, idtoken)

    return redirect('home:displaybook')

@login_required   
def addcourse(request):
    if request.method == 'GET':
        return render(request, "home/addcourse.html")

    else:
        print("falak")
        course_name = request.POST.get('course_name')
        video_name = request.POST.get('video_name')
        tags = request.POST.get('tags')
        upload=request.FILES.get('url')
        print(upload)


        try:
            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId']
            # a contains local id
        except:
            return render(request, "accounts/login.html")

        storage = firebase.storage()
        
        storage_path = "videos/"+course_name+"/"+video_name+".mp4"
        storage.child(storage_path).put(upload,idtoken)
        url = storage.child(storage_path).get_url(idtoken)

        username = database.child("users").child(a).child("details").child("username").get(idtoken).val()
        #print(username)
        data = {
            "tags": tags,
            "url": url,
            "username": username,
        }

        database.child('course').child(course_name).child(video_name).set(data, idtoken)
        return render(request, "home/courses.html")
@login_required
def course_list(request):
    courses = database.child('course').shallow().get().val()
    print(courses)
    list_courses = [*courses]
    print(list_courses)
    link_lists = []
    for i in list_courses:
        videos = database.child('course').child(i).shallow().get().val()
        videos1=[*videos]
        link = "/stuff/"+i+"/"+videos1[0]
        link_lists.append(link)
    print(link_lists)
    combine_list = zip(list_courses,link_lists)
    return render(request, "home/display_courses.html", {'combine_list':combine_list})
@login_required
def viewcourse(request,coursename,videoname):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        # a contains local id
    except:
        return render(request, "accounts/login.html")
    videos = database.child('course').child(coursename).shallow().get(idtoken).val()
    videos1=[*videos]
    link_list=[]
    for i in videos1:
        link = "/stuff"+"/"+coursename+"/"+i
        link_list.append(link)

    url= database.child('course').child(coursename).child(videoname).child('url').get(idtoken).val()

    combine_list = zip(videos1,link_list)
    return render(request, "home/video_page.html", {'combine_list':combine_list,"coursetitle":coursename,"videotitle":videoname,"url":url})

    
@login_required
def addexternalcourse(request):
    if request.method == 'GET':
        return render(request, "home/addexternalcourses.html")

    else:
        print("falak")
        course_name = request.POST.get('course_name')
        link = request.POST.get('link')
        tags = request.POST.get('tags')


        try:
            idtoken = request.session['uid']
            a = authe.get_account_info(idtoken)
            a = a['users']
            a = a[0]
            a = a['localId']
            # a contains local id
        except:
            return render(request, "accounts/login.html")

        username = database.child("users").child(a).child("details").child("username").get(idtoken).val()
        #print(username)
        data = {
            "tags": tags,
            "link": link,
            "username": username,
        }

        database.child('externalcourses').child(course_name).set(data, idtoken)
        return render(request, "home/courses.html")

 
@login_required
def external_course_list(request):  
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        # a contains local id
    except:
        return render(request, "accounts/login.html")
    courses = database.child('externalcourses').shallow().get(idtoken).val()
    print(courses)
    list_courses = [*courses]
    print(list_courses)
    link_lists = []
    
    for i in list_courses:
        link = database.child('externalcourses').child(i).child('link').get(idtoken).val()
        link_lists.append(link)
    print(link_lists)
    combine_list = zip(list_courses,link_lists)
    return render(request, "home/externalcourses.html", {'combine_list':combine_list})        

    
@login_required
def view_requests(request):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
    except:
        return render(request, "accounts/signup.html")

    all_requests = database.child("requests").shallow().get().val()
    print(all_requests)
    if all_requests is None:
        return render(request, "home/viewrequests.html", {'message': 'no requests'})

    all_requests_list = [*all_requests]
    print(all_requests_list)
    my_requests = []
    username = database.child("users").child(a).child("details").child("username").get(idtoken).val()
    print(username)
    for i in all_requests_list:
        if username == database.child('requests').child(i).child('owner').get().val():
            my_requests.append(i)
    print(my_requests)


    req_user = []
    status = []
    book_title = []
    req_id = []
    for i in my_requests:
        req_user1 = database.child('requests').child(i).child('req_user').get().val()
        req_user.append(req_user1)
        status1 = database.child('requests').child(i).child('status').get().val()
        status.append(status1)
        book_title1 = database.child('requests').child(i).child('book_title').get().val()
        book_title.append(book_title1)
        req_id.append(i)
    print(req_user)
    print(book_title)
    combine_list = zip(req_user,status,book_title,req_id)
    return render(request, "home/viewrequests.html", {'combine_list': combine_list, 'username':username})


k = 0;
@login_required
def updatet(request,book_title,req_id,req_user,username):

    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
    except:
        return render(request, "accounts/signup.html")

    database.child("books").child(book_title).update({"status": 0})
    database.child("requests").child(req_id).remove()
    reply = str("Your approval for book ") + str(book_title) + str("is accepted by ") + str(username)
    global k
    k = k+1
    data = {
        "reply" : reply,
        "to" : req_user,
        "from": username,
        "book_title":book_title,
    }
    database.child("notifications").child(k).set(data, idtoken)
    return redirect("home:view_requests")
@login_required
def updatef(request,book_title,req_id,req_user,username):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
    except:
        return render(request, "accounts/signup.html")


    database.child("requests").child(req_id).remove()
    reply = str("Your approval for book ") + str(book_title) + str("is declined by ") + str(username)
    global k
    k = k + 1
    data = {
        "reply": reply,
        "to": req_user,
        "from": username,
        "book_title": book_title,
    }
    database.child("notifications").child(k).set(data, idtoken)
    return redirect("home:view_requests")
@login_required
def notifications(request):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
    except:
        return render(request, "accounts/signup.html")

    all_reply = database.child("notifications").shallow().get().val()
    print(all_reply)
    if all_reply is None:
        return render(request, "home/viewrequests.html", {'message': 'no requests'})

    all_reply_list = [*all_reply]
    print(all_reply)
    my_reply = []
    n_id = []
    username = database.child("users").child(a).child("details").child("username").get(idtoken).val()
    print(username)
    for i in all_reply_list:
        if username == database.child('notifications').child(i).child('to').get().val():
            my_reply.append(i)

    print(my_reply)


    users = []
    for i in my_reply:
        users1 = database.child('notifications').child(i).child('from').get().val()
        users.append(users1)
        n_id.append(i)

    mystr = []
    for i in my_reply:
        users1 = database.child('notifications').child(i).child('reply').get().val()
        mystr.append(users1)

    mybooks = []
    for i in my_reply:
        book = database.child('notifications').child(i).child('book_title').get().val()
        mybooks.append(book)

    combine_list = zip(my_reply, users,n_id,mystr,mybooks)
    return render(request, "home/notifications.html", {'combine_list': combine_list})
@login_required
def n_delete(request,n_id):
    database.child("notifications").child(n_id).remove()
    return redirect("home:notifications")
