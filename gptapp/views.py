import g4f
from g4f.client import Client
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class AskView(APIView):
    
    context = []
    client = Client(
      provider=g4f.Provider.RetryProvider([g4f.Provider.Chatgpt4o, g4f.Provider.Chatgpt4Online, g4f.Provider.Liaobots, g4f.Provider.Nexra], shuffle=False)
    )

    def post(self, request):
        try:
            question = request.data.get('question')
            if not question:
                return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            self.context.append({"role": "user", "content": question})


            response = client.chat.completions.create(
                model=g4f.models.default,
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
