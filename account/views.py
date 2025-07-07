from django.db.models import Count, Q
from django.shortcuts import render
import requests
from django.http import JsonResponse

from account.models import GamAccount , UnsentLetter


def letter_delivery(request):
    # Annotate only unsent letters per user
    user_data = GamAccount.objects.annotate(
        letter_count=Count('user_letter', filter=Q(user_letter__sent=False))
    ).filter(
        letter_count__gt=0
    )

    user_info = []
    for user in user_data:
        user_info.append({
            "username": user.username,
            "letter_count": user.letter_count,
            "desktop_ip": user.desktop_ip
        })

        UnsentLetter.objects.filter(user=user, sent=False).update(sent=True)

    # Send notifications
    for user in user_info:
        print('send notif')
        try:
            response = requests.post(
                f"http://{user['desktop_ip']}:5000",
                json={
                    'letter_count': user['letter_count'],
                    'username': user['username']
                },
                timeout=5
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send notification to {user['username']}: {e}")

    return JsonResponse(user_info, safe=False)
