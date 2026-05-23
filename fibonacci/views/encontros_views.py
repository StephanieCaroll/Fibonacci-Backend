# fibonacci/views/encontros_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Exposicao 
from ..serializers import ExposicaoSerializer

@api_view(['GET'])
def getEncontros(request):
    encontros = Exposicao.objects.all()
    serializer = ExposicaoSerializer(encontros, many=True)
    return Response(serializer.data)