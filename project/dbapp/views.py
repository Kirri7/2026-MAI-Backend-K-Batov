from django.db import IntegrityError, transaction
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST
from .models import Course, User, UserProfile


@require_GET
def search_courses(request: HttpRequest):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'error': 'Parameter "q" is required'}, status=400)

    courses = Course.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(author__username__icontains=query)
    ).values('id', 'title', 'description', 'author__username')

    data = {'results': list(courses)}
    return JsonResponse(data)


@require_GET
def list_courses(request):
    courses = Course.objects.all()
    data = {'results': list(courses.values('id', 'title', 'description'))}
    return JsonResponse(data)


@require_POST
def create_course(request: HttpRequest):
    try:
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        author_id = request.POST.get('author_id', '').strip()

        if not title or not author_id:
            return JsonResponse({'error': 'Title and author_id are required'}, status=400)

        author = User.objects.get(id=author_id)

        course = Course.objects.create(
            title=title,
            description=description,
            author=author
        )

        return JsonResponse({
            'id': course.id,    # type: ignore
            'title': course.title,
            'message': 'Course created successfully'
        }, status=201)

    except User.DoesNotExist:
        return JsonResponse({'error': 'Bad author_id'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# curl -X POST http://127.0.0.1:8000/dbapp/courses/create \
# -d "title=Python Django" \
# -d "description=For beginners" \
# -d "author_id=1"


@require_POST
def create_user(request: HttpRequest):
    try:
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        bio = request.POST.get('bio', '').strip()

        if not username or not email:
            return JsonResponse({'error': 'Username and email are required'}, status=400)

        with transaction.atomic():
            user = User.objects.create(
                username=username,
                email=email
            )
            UserProfile.objects.create(
                user=user,
                phone_number=phone,
                bio=bio if bio else None
            )

        return JsonResponse({
            'id': user.id,    # type: ignore
            'email': user.email,
            'phone': user.profile.phone_number,    # type: ignore
            'message': 'User created successfully'
        }, status=201)

    except IntegrityError as e:
        error_msg = str(e)
        if 'username' in error_msg or 'email' in error_msg:
            return JsonResponse({'error': 'Username or email already exists'}, status=400)
        return JsonResponse({'error': 'Database error'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# curl -X POST http://127.0.0.1:8000/dbapp/users/create \
# -d "username=user1" \
# -d "email=user1@mail.org"
