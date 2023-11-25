from django.http import JsonResponse
import json

def validate_post_create(func):
    def wrapper(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            if 'title' not in data or 'content' not in data:
                return JsonResponse({'error': '입력 데이터가 올바르지 않습니다.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': '입력 데이터가 올바르지 않습니다.'}, status=400)

        return func(request, *args, **kwargs)
    return wrapper
