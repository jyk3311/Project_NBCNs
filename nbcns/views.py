from .models import NBCN, NBCN_Bookmark
from rest_framework.permissions import BasePermission, IsAuthenticated
from .functions import NBCNGpts, fetch_title_and_clean_content  # 함수 임포트
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import NBCNSerializer

# 사용자 권한을 정의하는 클래스
class IsSuperuserForWriteOperations(BasePermission):
    def has_permission(self, request, view):
        # POST와 DELETE 요청에 대해서는 사용자가 최고 관리자인지 검사
        if request.method in ('POST', 'DELETE'):
            return request.user and request.user.is_superuser
        # 그 외의 요청은 인증된 사용자면 허용
        return request.user and request.user.is_authenticated


# NBCN 목록을 조회 / 생성
class NBCNListCreateAPIView(APIView):
    permission_classes = [IsSuperuserForWriteOperations]  # 특정 권한 클래스를 적용하여 권한 설정

    # 모든 NBCN 객체를 조회하는 메서드 (GET 요청 처리)
    def get(self, request):
        nbcns = NBCN.objects.all()
        serializer = NBCNSerializer(nbcns, many=True)
        return Response(serializer.data)

    # 새로운 NBCN 객체를 생성하는 메서드 (POST 요청 처리)
    def post(self, request, *args, **kwargs):
        # 'link' 필드만 필수로 처리
        link = request.data.get('link')
        if not link:
            return Response({"error": "link 필드는 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # link가 있을 경우, 나머지 필드를 자동으로 생성
        title, cleaned_text = fetch_title_and_clean_content(link)  # 링크로부터 제목과 정리된 텍스트를 가져오는 함수 호출
        content = NBCNGpts(cleaned_text)  # 클린업된 내용을 요약하는 함수 호출

        # 생성된 데이터를 사용하여 NBCN 인스턴스를 생성
        serializer = NBCNSerializer(data={
            'title': title,
            'link': link,
            'content': content
        })

        # 직렬화 데이터가 유효성 체크 저장 그리고 응답 반환
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# NBCN 조회 / 삭제
class NBCNDetailAPIView(APIView):

    permission_classes = [IsSuperuserForWriteOperations]  # 특정 권한 클래스를 적용하여 권한 설정

    # 특정 NBCN 조회
    def get(self, request, pk):
        nbcn = get_object_or_404(NBCN, pk=pk)
        serializer = NBCNSerializer(nbcn)
        return Response(serializer.data)

    # 특정 NBCN 삭제
    def delete(self, request, pk):
        nbcn = get_object_or_404(NBCN, pk=pk)
        nbcn.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# NBCN 북마크
class NBCNBookmarkAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    # 특정 NBCN 객체를 북마크하거나 삭제하는 메서드 (POST 요청 처리)
    def post(self, request, pk):
        nbcn = get_object_or_404(NBCN, pk=pk)  # pk로 NBCN 객체를 찾거나 404 오류 반환
        bookmark, created = NBCN_Bookmark.objects.get_or_create(user=request.user, NBCN=nbcn)  # 북마크 객체 생성 또는 검색

        if created:
            # 북마크가 새로 생성된 경우
            return Response({"message": "북마크 추가"}, status=status.HTTP_201_CREATED)
        else:
            # 이미 존재하는 경우 삭제
            bookmark.delete()
            return Response({"message": "북마크가 삭제되었습니다."}, status=status.HTTP_200_OK)
