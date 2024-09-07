from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import g4f

@method_decorator(csrf_exempt, name='dispatch')
class AskView(APIView):
    def post(self, request):
        try:
            question = request.data.get('question')
            if not question:
                return self._create_response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Запрос к API g4f
            response = g4f.ChatCompletion.create(model=g4f.models.gpt_4o_mini, messages=[{"role": "user", "content": question}])

            # Проверка и обработка ответа
            if isinstance(response, str):
                gpt_response = response
            else:
                return self._create_response({"error": "Unexpected response format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not gpt_response:
                return self._create_response({"error": "Failed to get a response from GPT-4"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return self._create_response({"answer": gpt_response}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in AskView: {e}")  # Отладка ошибок
            return self._create_response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _create_response(self, data, status):
        response = JsonResponse(data, status=status)
        response["Access-Control-Allow-Origin"] = "https://g-gpt.vercel.app"
        return response

