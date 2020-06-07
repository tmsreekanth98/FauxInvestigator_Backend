from rest_framework import serializers
from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):

	class Meta:
		model = Analysis
		fields = ('text','author','label','pants_on_fire','false','barely_true','half_true','mostly_true','true')