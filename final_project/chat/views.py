from django.shortcuts import render

# dummy data
posts = [
    {
        'author': 'matthew',
        'title': 'the day',
        'content': 'the content'
    },
{
        'author': 'jane',
        'title': 'the day',
        'content': 'the content'
    }
]


def home(request):
    context = {
        'post': posts
    }
    return render(request, 'chat/home.html', context)


def about(request):
    return render(request, 'chat/about.html', {'title': 'About'})
