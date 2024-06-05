from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .models import GeneratedVideo

import base64

import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


my_api_key = "sk-k1T17P9dOVdkdHF1Cx03YB9uKvtitMfNs0AF0OMXzauk6Dzt"

class ImageToVideoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        image_data = request.data.get('image')
        seed = request.data.get('seed', 0)
        cfg_scale = request.data.get('cfg_scale', 1.8)
        motion_bucket_id = request.data.get('motion_bucket_id', 127)

        # 获取用户信息
        user = request.user

        # 调用 stable-vedio-diffusion API 生成视频
        response = requests.post(
            "https://api.stability.ai/v2beta/image-to-video",
            headers={"authorization": f"Bearer {my_api_key}"},
            files={"image": base64.b64decode(image_data)},
            data={"seed": seed, "cfg_scale": cfg_scale, "motion_bucket_id": motion_bucket_id}
        )

        if response.status_code == 200:
            generation_id = response.json().get('id')
            GeneratedVideo.objects.create(user=user, generation_id=generation_id)
            return Response({
                "message": "Video generation started. Poll for results using the id in the response here.",
                "generation_id": generation_id
            }, status=status.HTTP_200_OK)
        elif response.status_code == 400:
            print(response.json().get('errors'))
            
            return Response({
                "error": "Invalid parameter(s), see the errors field for details.",
                "details": response.json().get('errors')
            }, status=status.HTTP_400_BAD_REQUEST)
        elif response.status_code == 403:
            return Response({
                "error": "Your request was flagged by our content moderation system."
            }, status=status.HTTP_403_FORBIDDEN)
        elif response.status_code == 413:
            return Response({
                "error": "Your request was larger than 10MiB."
            }, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        elif response.status_code == 422:
            return Response({
                "error": "You made a request with an unsupported language."
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif response.status_code == 429:
            return Response({
                "error": "You have made more than 150 requests in 10 seconds."
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        elif response.status_code == 500:
            return Response({
                "error": "Stable Vedio：An internal error occurred. If the problem persists contact support."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "error": "Failed to generate video"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class VideoStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        videos = GeneratedVideo.objects.filter(user=user)

        # 检查每个视频的状态并更新数据库
        for video in videos:
            if video.status == 'in-progress':
                response = requests.get(
                    f"https://api.stability.ai/v2beta/image-to-video/result/{video.generation_id}",
                    headers={
                        'accept': 'application/json',
                        "authorization": f"Bearer {my_api_key}"
                    }
                )

                if response.status_code == 200:
                    video.status = 'complete'
                    video.video_data = response.json().get('video')
                    video.seed = response.json().get('seed')
                    video.save()
                elif response.status_code == 202:
                    continue
                elif response.status_code == 404:
                    video.status = 'expired'
                    video.save()

        # 获取更新后的所有视频信息
        updated_videos = GeneratedVideo.objects.filter(user=user).values('generation_id', 'status')

        return JsonResponse({"videos": list(updated_videos)}, status=200)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import GeneratedVideo

class VideoDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        generation_id = request.query_params.get('generation_id')
        
        if not generation_id:
            return Response({"error": "generation_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = GeneratedVideo.objects.get(generation_id=generation_id, user=request.user)
        except GeneratedVideo.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "generation_id": video.generation_id,
            "status": video.status,
            "video_data": video.video_data
        }, status=status.HTTP_200_OK)
