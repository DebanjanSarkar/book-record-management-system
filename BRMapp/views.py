from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from BRMapp import models,forms

# Create your views here.

@csrf_exempt
def userLogin(request):
    data = {}
    if request.method=="POST":
        username = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request,username=username,password=passwd)
        if user != None:
            login(request,user)
            request.session['user_name'] = username             #It stores the username in session variable
            return HttpResponseRedirect('/BRMapp/view-books')
        else:
            data['error']="Incorrect Username or Password !"
            res = render(request,'BRMapp/user_login.html',data)
            return res
    else:
        res = render(request,'BRMapp/user_login.html',data)
        return res

@login_required(login_url="/BRMapp/login")
def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/BRMapp/login')

@login_required(login_url="/BRMapp/login")
def newBook(request):
    form = forms.NewBookForm()
    res = render(request,'BRMapp/new-book.html',{'form':form,'user_name':request.session['user_name']})
    return res

@login_required(login_url="/BRMapp/login")
def add(request):
    if request.method=='POST':
        form = forms.NewBookForm(request.POST)
        book = models.Book()
        book.title = form.data['title']
        book.price = form.data['price']
        book.author = form.data['author']
        book.publisher = form.data['publisher']
        book.save()
        s = """
        <center>
        <h1>The New Book Record is being sucessfully saved!</h1>
        <h4><a href="/BRMapp/view-books">View All Books</a></h4>
        </center>
        """
        return HttpResponse(s)

@login_required(login_url="/BRMapp/login")
def viewBooks(request):
    books = models.Book.objects.all()
    if(len(books)==0):
        res = render(request,'BRMapp/view-books.html',{'user_name':request.session['user_name']})
    else:
        res = render(request,'BRMapp/view-books.html',{'books':books,'user_name':request.session['user_name']})
    return res

@login_required(login_url="/BRMapp/login")
def editBook(request):
    if request.method=='GET':
        bookid = request.GET['bookid']
        book = models.Book.objects.get(id=bookid)
        book_details = {
            'title':book.title,
            'price':book.price,
            'author':book.author,
            'publisher':book.publisher
        }
        form = forms.NewBookForm(initial=book_details)
        res = render(request,'BRMapp/edit-book.html',{'form':form,'book':book,'user_name':request.session['user_name']})
        return res

@login_required(login_url="/BRMapp/login")
def edit(request):
    if request.method=='POST':
        bookid = request.POST['bookid']
        form = forms.NewBookForm(request.POST)
        book = models.Book()
        book.id = bookid
        book.title = form.data['title']
        book.price = form.data['price']
        book.author = form.data['author']
        book.publisher = form.data['publisher']
        book.save()
        return HttpResponseRedirect('/BRMapp/view-books')

@login_required(login_url="/BRMapp/login")
def deleteBook(request):
    bookid = request.GET['bookid']
    book = models.Book.objects.filter(id=bookid)
    book.delete()
    return HttpResponseRedirect('BRMapp/view-books')

@login_required(login_url="/BRMapp/login")
def searchBook(request):
    form = forms.SearchForm()
    res = render(request,'BRMapp/search-book.html',{'form':form,'user_name':request.session['user_name']})
    return res

@login_required(login_url="/BRMapp/login")
def search(request):
    if request.method=='POST':
        form = forms.SearchForm(request.POST)
        all_books = models.Book.objects.all()
        matching_books = []
        for bk in all_books:
            t = str(bk.title)
            if t.lower()==form.data['title'].lower():
                matching_books.append(bk)
        if(len(matching_books)>0):
            res = render(request,'BRMapp/search-book.html',{'form':form,'books':matching_books,'user_name':request.session['user_name']})
        else:
            res = render(request,'BRMapp/search-book.html',{'form':form,'user_name':request.session['user_name']})
        return res

# def search(request):
#     if request.method=='POST':
#         form = forms.SearchForm(request.POST)
#         books = models.Book.objects.filter(title=form.data['title'])
#         if(len(books)>0):
#             res = render(request,'BRMapp/search-book.html',{'form':form,'books':books})
#         else:
#             res = render(request,'BRMapp/search-book.html',{'form':form,'no_book':'0'})
#         return res
