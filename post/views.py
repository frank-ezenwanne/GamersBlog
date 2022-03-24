from django.shortcuts import render, get_object_or_404,redirect
from .forms import CreatePostForm,CommentForm,PostUpdateForm
from .models import Post,Comment
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
#from operator import attrgetter
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import random

def home(request):
	return render(request,'post/home.html')


@login_required
def create_post_view(request):
	if request.method == 'POST':
		form = CreatePostForm(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			return redirect(instance.get_absolute_url())
	else:
		form = CreatePostForm()
	return render(request,'post/post_form.html',{"form":form})
	


def do_search(query):
	if query != None and query != "":
		query_split = query.split(" ")
		for q in query_split:
			search_results = Post.objects.filter(Q(title__icontains = q)|Q(slug__icontains = q)|Q(content__icontains = q)|Q(game_name__icontains = q)|Q(game_console__icontains = q)).distinct().order_by("-date_posted")
			
	else:
		q=""
		search_results = Post.objects.filter(Q(title__icontains = q)|Q(slug__icontains = q)|Q(content__icontains = q)|Q(game_name__icontains = q)|Q(game_console__icontains = q)).distinct().order_by("-date_posted")
		
	return search_results
		



def do_user_search(query):
	the_queryset = []
	if query != None and query != "":
		counter = 0
		query_split = query.split(" ")
		for q in query_split:
			counter += 1
			search_results = User.objects.filter(Q(username__icontains = q) & ~Q(username__iexact = "sherlock_of_zen")).distinct()
			if counter >= 15:
				break
		for search in search_results:
			the_queryset.append(search)
		
	return list(set(the_queryset))
		

def PostListView(request):
		page = request.GET.get('page',1)
		query = request.GET.get('query',"")
		search_select = request.GET.get("selectedValue","posts")

		if search_select == "users":
			users  = do_user_search(query)
			context = {"users":users, "query":query,"search_select":"users"}
			
			
		else:
			#posts = (sorted(do_search(query), key = attrgetter('date_posted'),reverse = True))
			posts = do_search(query)
			paginator = Paginator(posts,8)
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)
			except:
				posts = paginator.page(1)
			context = {"posts":posts,"query":query,"search_select":"posts"}
			
		return render(request,"post/post_listin.html",context)
	
@login_required
def GetLikedPosts(request,username):
	if request.method == "GET":
		post_user = get_object_or_404(User, username = username)
		posts = Post.objects.filter(likes = post_user)
		paginator = Paginator(posts,8)
		page = request.GET.get('page',1)
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)
		except:
			posts = paginator.page(1)
		return render(request,"post/liked_posts.html",{"posts":posts,"post_user":post_user})




@login_required
def CommentDeleteView(request,username,slug,commenter,comment_id):
	if request.method == 'GET':
		author = User.objects.filter(username = username).first()
		post = get_object_or_404(Post,author = author.id, slug = slug)
		if commenter == request.user.username:
			com_del = get_object_or_404(Comment,id=comment_id)
			com_del.comment_body = '*deleted-comment*'
			com_del.save()
	return redirect(post.get_absolute_url())
			
@login_required		
def PostLikeView(request,username,slug):
	if request.method == 'GET' or (request.method == 'GET' and request.is_ajax()):
		author = User.objects.filter(username = username).first()
		post = get_object_or_404(Post,author = author.id, slug = slug)
		if request.user in post.likes.all():
			post.likes.remove(request.user)
		else:
			post.likes.add(request.user)

		if request.is_ajax():
			if request.user in post.likes.all():
				present = "true"
			else:
				present = "false"
			likes_count = post.likes.count()
			return JsonResponse({"likes_count":likes_count,"present":present})

	return redirect(post.get_absolute_url())
			
			
		

@login_required
def CommentLikeView(request,username,slug,comment_id):
	if request.method == 'GET' or (request.method == 'GET' and request.is_ajax()):
		comment =  get_object_or_404(Comment, id = comment_id)
		author = User.objects.filter(username = username).first()
		post = get_object_or_404(Post,author = author.id, slug = slug)
		if request.user in comment.likes.all():
			comment.likes.remove(request.user)
		else:
			comment.likes.add(request.user)

		if request.is_ajax():
			if request.user in comment.likes.all():
				present = "true"
			else:
				present = "false"
			likes_count = comment.likes.count()
			return JsonResponse({"likes_count":likes_count,"present":present})
	return redirect(post.get_absolute_url())

def PostDetailView(request,username,slug):
	user_name = User.objects.filter(username = username).first()
	post = get_object_or_404(Post,author = user_name.id, slug = slug)
	comments=Comment.objects.filter(post=post).order_by('date_posted')
	
	if request.method == 'POST':
		post_data = request.POST.copy()
		repliedcomid = post_data.get("repliedcomid",None)
		if repliedcomid != None and repliedcomid != "" :
			repliedcomid = int(int(repliedcomid)/2)
			post_data["repliedcomid"] = repliedcomid
		comment_form = CommentForm(post_data)
		
		if comment_form.is_valid():
			comment_body = comment_form.cleaned_data['comment_body']
			poster = request.user
			if comment_form.cleaned_data['repliedcomid']:
				replied_commentid = comment_form.cleaned_data['repliedcomid']
				comment = Comment.objects.create(post=post,commenter=poster,comment_body=comment_body,repliedcomid=replied_commentid)
			else:
				comment = Comment.objects.create(post=post,commenter=poster,comment_body=comment_body)
			comment.save()	
	else:
		comment_form=CommentForm()
	miss_combo = []
	get_most_liked = Post.objects.all().order_by("-likes")[:15]
	get_most_recent = Post.objects.all().order_by("-date_posted")[:10]
	for elem in get_most_liked:
		miss_combo.append(elem)
	for elem in get_most_recent:
		miss_combo.append(elem)
	miss_combo = list(set(miss_combo))
	random.shuffle(miss_combo)
	if post in miss_combo:
		miss_combo.remove(post)
	miss_combo = miss_combo[:5]

	return render(request,'post/post_detail.html',
		context={'comments':comments,
				'post':post,
				'miss_combo' : miss_combo,
				'comment_form':comment_form

		})


def UserPostListView(request,username):
	user = get_object_or_404(User, username = username)
	posts = Post.objects.filter(author = user).order_by('-date_posted')
	post_num = posts.count()
	paginator = Paginator(posts,8)
	page = request.GET.get('page',1)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	except:
		posts = paginator.page(1)


	return render(request,"post/user_post_list.html",{"posts":posts,"post_user":user,"post_num":post_num})
			
@login_required
def UserPostComView(request,username):
	user = get_object_or_404(User,username = username)
	posts = Post.objects.filter(comment__commenter = user.id).distinct()
	post_num = posts.count()
	paginator = Paginator(posts,8)
	page = request.GET.get('page',1)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	except:
		posts = paginator.page(1)

	return render(request,"post/post_user_com.html",{"posts":posts,"com_user":user,"post_num":post_num})



@login_required
def PostUpdateView(request,username,slug):
	user = get_object_or_404(User, username = username)
	post = get_object_or_404(Post,author = user.id,slug = slug)
	if request.method == 'POST':
		if post.author == request.user:
			form = CreatePostForm(request.POST,request.FILES,instance = post)
			if form.is_valid():
				form.save()
	else:
		form = CreatePostForm(instance = post)
		return render(request,'post/post_update.html',{'form':form})
					
	return redirect(post.get_absolute_url())



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	template_name = "post/post_confirm_del.html"
	context_object_name = 'post'
	success_url = '/posts'

	def test_func(self):
		post = self.get_object()
		if post.author == self.request.user:
			return True
		return False


def ConsoleListView(request,game_console):
	posts = Post.objects.filter(game_console = game_console).order_by('-date_posted')
	paginator = Paginator(posts,8)
	page = request.GET.get('page',1)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	except:
		posts = paginator.page(1)

	return render(request,"post/console_post_list.html",{"posts":posts,"game_console":game_console})
