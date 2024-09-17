import g4f
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class AskView(APIView):
    
    context = []


    def post(self, request):
        try:
            question = request.data.get('question')
            if not question:
                return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            self.context.append({"role": "user", "content": question})


            response = g4f.ChatCompletion.create(
                model='gpt-4-turbo',
                messages=self.context
            )
            
            
            if isinstance(response, str):
                gpt_response = response
            else:
                return Response({"error": "Unexpected response format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not gpt_response:
                return Response({"error": "Failed to get a response from GPT-4"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            self.context.append({"role": "assistant", "content": gpt_response})

            return Response({"answer": gpt_response}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in AskView: {e}")  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
