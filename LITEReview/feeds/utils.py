from django.contrib.auth.models import User

from feeds.models import Review, Ticket
from follow_auth.models import UserFollows


def get_viewable_reviews(user: User):
    """
    All viewable reviews for user feed:
    """
    followed_users = get_follows(user)
    followed_users.append(user)

    reviews = []
    all_reviews = Review.objects.filter(user__in=followed_users).distinct()
    for review in all_reviews:
        reviews.append(review.id)

    user_tickets = Ticket.objects.filter(user=user)
    for ticket in user_tickets:
        review_responses = Review.objects.filter(ticket=ticket)
        for review in review_responses:
            reviews.append(review.id)

    reviews = Review.objects.filter(id__in=reviews).distinct()

    return reviews


def get_viewable_tickets(user: User):
    """
    All viewable tickets for user feed:
    """
    followed_users = get_follows(user)
    followed_users.append(user)

    tickets = Ticket.objects.filter(user__in=followed_users)
    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied and replied.user in followed_users:
                tickets = tickets.exclude(id=ticket.id)

        except Review.DoesNotExist:
            pass

    return tickets

def get_replied_tickets(tickets):
    """
    Get tickets with review response
    """
    replied_tickets = []
    replied_reviews = []

    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied:
                replied_tickets.append(replied.ticket)
                replied_reviews.append(replied)

        except Review.DoesNotExist:
            pass

    return replied_tickets, replied_reviews

def get_follows(user):
    
    follows = UserFollows.objects.filter(user=user)
    followed_users = []
    for follow in follows:
        followed_users.append(follow.followed_user)

    return followed_users