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
from .utils import (get_viewable_reviews, get_viewable_tickets, get_replied_tickets, get_follows)



@login_required
def feeds(request):
    followed_users = get_follows(request.user)

    reviews = get_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    context = {
        'posts': posts,
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'title': 'Feed',
        'followed_users': followed_users
    }

    return render(request, 'feeds/feeds.html', context)


@login_required
def user_posts(request, pk=None):
    if pk:
        user = get_object_or_404(User, id=pk)
    else:
        user = request.user

    followed_users = get_follows(request.user)

    reviews = Review.objects.filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
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



@login_required
def create_review(request):
    if request.method == 'POST':
        t_form = TicketForm(request.POST, request.FILES)
        r_form = ReviewForm(request.POST)

        if t_form.is_valid() and r_form.is_valid():
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
        'title': 'New Review'
    }

    return render(request, 'feeds/create_review.html', context)


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
        'title': 'New Ticket'
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

    return render(request, 'reviews/post_detail.html', context)




    
