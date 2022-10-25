from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
from itertools import chain
from django.contrib.auth.decorators import login_required


@login_required
def feeds(request):
    tickets = models.Ticket.objects.all() 
    reviews = models.Review.objects.all()

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    return render(request, "feeds/feeds.html")
    

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
        'feeds/create_ticket.html',
        context
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

