from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import g4f

class AskView(APIView):
    def post(self, request):
        try:
            question = request.data.get('question')
            if not question:
                return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Запрос к API g4f
            response = g4f.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])

            # Проверка и обработка ответа
            if isinstance(response, str):
                gpt_response = response
            else:
                return Response({"error": "Unexpected response format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not gpt_response:
                return Response({"error": "Failed to get a response from GPT-3.5-turbo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"answer": gpt_response}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in AskView: {e}")  # Отладка ошибок
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
