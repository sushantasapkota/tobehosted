from django.shortcuts import render, redirect
from . models import Posts
from . models import organizations
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
import stripe
from django.core.paginator import Paginator

stripe.api_key = "sk_test_51HniMuJ1JQRUeJxSE0BjVkf2qs2aWYFAOVdwQiqtKMCwB935ZyW6ktrg42860Ipvs6ObijR5xu8zCdTDc5s26JD700chx3IeJX"
# Create your views here.
def home(request):
    posts = Posts.objects.all()
    organization = organizations.objects.all()
    total_organization = organization.count()
    total_post = posts.count()
    context = {
        'total_posts':total_post,
        'total_organization':total_organization
    }
    return render (request,'post/home.html',context)

def explore(request):

    posts = Posts.objects.all().order_by('-id')

    organization = organizations.objects.all()

    paginator = Paginator(posts,4)
    page = request.GET.get('page') #?page=2
    posts = paginator.get_page(page)

    return render(request,'post/explore.html',{'posts':posts,'organizations':organization})

# class PostListView(ListView):
#     model = {
# 		'Posts':Posts,
# 		'organizations':organizations}
#     template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']


class PostDetailView(DetailView):
    	model=Posts

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Posts
    fields = ['title', 'type_food','pickup_location','food_fresh','agegroupofclothes','served_people','Phone']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Posts
    if Posts.title == 'Food':
        fields = ['title', 'type_food','pickup_location','food_fresh','served_people','Phone']
    else:
        fields = ['title', 'type_food','pickup_location','food_fresh','agegroupofclothes','served_people','Phone']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def share(request):
    return render(request,'post/share.html')
@login_required
def explorepay(request):
	return render(request, 'post/index.html')

@login_required
def charge(request):
    

	if request.method == 'POST':
		print('Data:', request.POST)

		amount = int(request.POST['amount'])

		customer = stripe.Customer.create(
			email=request.POST['email'],
			name=request.POST['nickname'],
			source=request.POST['stripeToken']
			)

		charge = stripe.Charge.create(
			customer=customer,
			amount=amount*100,
			currency='usd',
			description="Donation"
			)

	return redirect(reverse('success', args=[amount]))

@login_required
def successMsg(request, args):
	amount = args
	return render(request, 'post/success.html', {'amount':amount})