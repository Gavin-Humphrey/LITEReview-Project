from itertools import chain
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from .forms import ReviewForm, TicketForm
from .models import Review, Ticket
from .utils import (get_view_reviews, get_view_tickets, get_replied_tickets, get_follows)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import DeleteView
from django.db.models import Q #



@login_required
def feeds(request):
    followed_users = get_follows(request.user)

    reviews = get_view_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_view_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    ####### Remove pagination here
    if posts_list:
        paginator = Paginator(posts_list, 3)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    context = {
        'posts': posts,
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'title': 'Feeds',
        'followed_users': followed_users
    }

    return render(request, 'feeds/feeds.html', context)
    ############

    ######### use if you want to remove pagination


"""return render(request, 'feeds/feeds.html', 
    context = {
        'posts': posts_list,
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'title': 'Feeds',
        'followed_users': followed_users
    })"""


@login_required
def user_posts(request, pk=None):
    if pk:
        user = get_object_or_404(User, id=pk)
    else:
        user = request.user

    followed_users = get_follows(request.user)

    reviews = Review.objects.filter(user=user)
    #reviews = Review.objects.filter(Q(user__in=followed_users) | Q(ticket__user=user))# added
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=user)
    #tickets = Review.objects.filter(Q(user__in=followed_users) | Q(review__user=user))# added
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)


    ### Remove Pagination
    if posts_list:
        paginator = Paginator(posts_list, 3)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        total_posts = paginator.count
    else:
        posts = None
        total_posts = 0

    context = {
        'posts': posts,
        'title': f"{user.username}'s posts ({total_posts})",
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'followed_users': followed_users
    }

    return render(request, 'feeds/feeds.html', context)

    ##############
    
    #### Use if you want to remove pagination
"""return render(request, 'feeds/feeds.html', 

    context = {
        'posts': posts_list,
        'title': f"{user.username}'s posts",
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'followed_users': followed_users
    })"""


@login_required
def create_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            try:
                image = request.FILES['image']
            except MultiValueDictKeyError:
                image = None

            t = Ticket.objects.create(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=image
            )
            t.save()
            Review.objects.create(
                ticket=t,
                user=request.user,
                headline=request.POST['headline'],
                body=request.POST['body']
            )
            messages.success(request, 'Your review has been posted!')
            return redirect('feeds-home')

    else:
        t_form = TicketForm()
        r_form = ReviewForm()

    context = {
        't_form': t_form,
        'r_form': r_form,
        'title': 'Post Review'
    }

    return render(request, 'feeds/create_review.html', context)


@login_required
def review_response(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            Review.objects.create(
                ticket=ticket,
                user=request.user,
                headline=request.POST['headline'],
                rating=request.POST['rating'],
                body=request.POST['body']
            )
            messages.success(request, f'Your response to "{ticket.title}" has been posted!')
            return redirect('feeds-home')

    else:
        r_form = ReviewForm()

    context = {
        'r_form': r_form,
        'post': ticket,
        'title': 'Response Review'
    }

    return render(request, 'feeds/create_review.html', context)



@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)
    if review.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        r_form = ReviewForm(request.POST, instance=review)

        if r_form.is_valid():
            r_form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('feeds-home')

    else:
        r_form = ReviewForm(instance=review)

    context = {
        'r_form': r_form,
        'post': review.ticket,
        'title': 'Update Review'
    }

    return render(request, 'feeds/create_review.html', context)


@login_required
def review_detail(request, pk):
    review = get_object_or_404(Review, id=pk)
    followed_users = get_follows(request.user)

    context = {
        'post': review,
        'title': 'Review detail',
        'followed_users': followed_users
    }

    return render(request, 'feeds/post_detail.html', context)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, f'Your review "{self.get_object().headline}" has been deleted.')
        return super(ReviewDeleteView, self).delete(request, *args, **kwargs)


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES.get('image', None)
            Ticket.objects.create(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=image
            )
            messages.success(request, 'Your ticket has been posted!')
            return redirect('feeds-home')

    else:
        form = TicketForm()

    context = {
        'form': form,
        'title': 'New Post'
    }

    return render(request, 'feeds/create_ticket.html', context)


@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    if ticket.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your ticket has been updated!')
            return redirect('feeds-home')

    else:
        form = TicketForm(instance=ticket)

    context = {
        'form': form,
        'title': 'Update Ticket'
    }

    return render(request, 'feeds/create_ticket.html', context)


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    followed_users = get_follows(request.user)

    replied_tickets, replied_reviews = get_replied_tickets([ticket])

    context = {
        'post': ticket,
        'title': 'Ticket detail',
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'followed_users': followed_users,
    }

    return render(request, 'feeds/post_detail.html', context)


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, f'Your ticket "{self.get_object().title}" has been deleted.')
        return super(TicketDeleteView, self).delete(request, *args, **kwargs)
