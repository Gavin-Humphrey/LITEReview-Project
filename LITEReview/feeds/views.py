from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from follow_auth.models import UserFollows




def dashboard(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()


    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    paginator = Paginator(tickets_and_reviews, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
  
    }

    return render(
        request,
        'feeds/feeds.html',
        context
    )



@login_required
def feeds(request):
    
    tickets = models.Ticket.objects.filter(
        user__in=request.user.follows.all()
    )
    reviews = models.Review.objects.filter(
        user__in=request.user.follows.all()  
    )
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    paginator = Paginator(tickets_and_reviews, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj
    }

    return render(
        request,
        "feeds/feeds.html",
        context
    )


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            if form.cleaned_data['image']:
                ticket.image = form.cleaned_data['image']
            ticket.save()
            return redirect('feeds-home')
    context = {
        'form': form
    }
    return render(
        request,
        'feeds/create_ticket.html', context
    )

@login_required
def create_review(request, ticket_id):
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = get_object_or_404(models.Ticket, id=ticket_id) 
            review.ticket.has_review = True
            review.ticket.save()
            review.save()
            return redirect('feeds-home')
    context = {
    'both': False,
    'form': form
    }
    return render(
        request,
        'feeds/create_review.html',
        context
    )



@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if ticket_form.cleaned_data['image']:
                ticket.image = ticket_form.cleaned_data['image']
            ticket.has_review = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = get_object_or_404(models.Ticket, id=ticket.id)
            review.save()
            return redirect('feed')
    context = {
        'both': True,
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(
        request,
        'feeds/feeds.html',
        context
    )


