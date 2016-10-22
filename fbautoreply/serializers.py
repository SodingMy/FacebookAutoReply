from rest_framework import serializers
from fbautoreply.models import ResponseMessage

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResponseMessage
        fields = ('message_text',)