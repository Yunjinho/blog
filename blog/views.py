from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogPost

def home(request):
    blogs = Blog.objects #쿼리셋#메소드
    #블로그 모든 글들을 대상으로
    blog_list= Blog.objects.all()
    #블로그 객체 세개를 한 페이지로 자르기
    paginator = Paginator(blog_list,5)
    #request된 페이지가 뭔지를 알아내고(request 페이지를 변수에 담아내고)
    page = request.GET.get('page')
    #request된페이지를 얻어온 뒤 return 해준다
    posts=paginator.get_page(page)

    return render(request, 'home.html',{'blogs':blogs,'posts':posts})

def detail(request,blog_id):
    blog_detail= get_object_or_404(Blog, pk =blog_id)#예외처리
    return render(request, 'detail.html',{'blog':blog_detail})

def new(request):#new.html을 띄워주는 함수
    return render(request,'new.html')

def create(request):#입력받은 내용을 데이터 베이스에 넣어주는 함수
    blog=Blog()
    blog.title=request.GET['title']
    blog.body=request.GET['body']
    blog.pub_date=timezone.datetime.now()
    blog.save()
    return redirect('home')
    
def blogpost(request):
    # 1.입력된 내용 처리->POST
    if request.method =='POST':
        form=BlogPost(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    # 2.빈 페이지를 띄워주는 기능->GET
    else :
        form =BlogPost()
        return render(request,'new.html',{'form':form})

def delete(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect('home')

def edit(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = BlogPost(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            # {'name': '수정된 이름', 'image': <InMemoryUploadedFile: Birman_43.jpg 	(image/jpeg)>, 'gender': 'female', 'body': '수정된 내용'}
            blog.title = form.cleaned_data['title']
            blog.body = form.cleaned_data['body']
            blog.save()
            return redirect('home')
        
    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = BlogPost()
        return render(request, 'edit_post.html',{'form':form})
