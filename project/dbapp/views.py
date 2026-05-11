from django.http.request import HttpRequest
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST
from .models import Course, User


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