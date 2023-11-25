from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from common.models import Post
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from collections import Counter
import logging
import json

from post.decorators import validate_post_create


# Create your views here.
logger = logging.getLogger('post')

@require_http_methods(["POST"])
@validate_post_create
def post_create(req):
    try:
        data = json.loads(req.body)

        title = data.get('title')
        content = data.get('content')
        words_counter = Counter(content.split())

        # 저장 및 연관 게시글 검색용 데이터 양식 준비
        most_common_words = words_counter.most_common()
        words_dict = dict(most_common_words)
        words_json = json.dumps(words_dict, ensure_ascii=False)

        new_post = Post(title=title, content=content, words=words_json)
        new_post.save()

        # 연관게시글 확인 로직 시작
        all_posts = Post.objects.all()

        new_post_words = set(words_dict.keys())
        zero_dict = {word: 0 for word in new_post_words}

        print(new_post_words)
        print(zero_dict)

        # 신규게시글의 단어들이 다른 게시글에 존재하는 횟수
        for word in new_post_words:
            for post in all_posts:
                post_words = json.loads(post.words)  
                if word in post_words:
                    zero_dict[word] += 1
           
                    
        print(zero_dict)
        # 60% 이상 나온 단어들은 연관단어에서 제외
        words_to_remove = set()
        for key, value in zero_dict.items():
            if value / len(all_posts) >= 0.6:
                words_to_remove.add(key)
        new_post_words -= words_to_remove

        # 신규게시글의 남은 단어가 2개 이상일때만 연관게시글이 존재할수있음
        if len(new_post_words) > 1:
            post

        print(new_post_words)

        

        result = {
            'message': f"{new_post.id}번 게시글이 저장되었습니다."
        }
        return JsonResponse(result)
    
    except Exception as e:
        logger.debug(e)
        result = {
            'message': '서버에 오류가 발생하였습니다.'
        }
        return JsonResponse(result)
    

def post_list(req):
    try:
        posts = Post.objects.all()
        posts_data = [[model_to_dict(post, exclude=["words"])] for post in posts]

        result = {
            'data': posts_data
        }
        return JsonResponse(result)
    
    except Exception as e:

        result = {
            'message': '서버에 오류가 발생하였습니다.'
        }
        return JsonResponse(result)
    
def post_detail(req, post_id):
    try:
        post = Post.objects.get(id=post_id)

        result = {
            'data': model_to_dict(post, exclude=["words"])
        }
        return JsonResponse(result)
    
    except ObjectDoesNotExist:
        return JsonResponse({'message': '해당 게시글을 찾을 수 없습니다.'})
    
    except Exception as e:

        result = {
            'message': '서버에 오류가 발생하였습니다.'
        }
        return JsonResponse(result)
    

