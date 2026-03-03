from rest_framework import serializers
from django.db import transaction
from paths.models import Path, Step, GPSPoint, Establishment
from paths.serializers.step_serializer import StepSerializer
from paths.serializers.gps_serializer import GPSPointSerializer

MAX_VIDEO_DURATION = 120

class PathCreateSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    gps_points = GPSPointSerializer(many=True, required=False)

    # Départ : soit label soit coordonnées
    start_label = serializers.CharField(required=False, allow_blank=True)
    start_lat = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    start_lng = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)

    # Destination : sera calculée à partir de l'établissement lié
    end_lat = serializers.DecimalField(max_digits=9, decimal_places=6, read_only=True)
    end_lng = serializers.DecimalField(max_digits=9, decimal_places=6, read_only=True)

    class Meta:
        model = Path
        fields = [
            'id',
            'title',
            'start_label',
            'start_lat',
            'start_lng',
            'end_lat',
            'end_lng',
            'video_url',
            'duration',
            'status',
            'is_official',
            'created_at',
            'steps',
            'gps_points',
        ]
        read_only_fields = ['status', 'is_official', 'created_at', 'end_lat', 'end_lng']

    def validate(self, data):
        # Vérifier que le départ est renseigné
        start_label = data.get('start_label')
        start_lat = data.get('start_lat')
        start_lng = data.get('start_lng')

        if not start_label and (start_lat is None or start_lng is None):
            raise serializers.ValidationError(
                "Vous devez renseigner soit start_label, soit start_lat et start_lng pour le départ."
            )

        # Vérification des étapes
        steps = data.get('steps', [])
        duration = data.get('duration')
        if not (2 <= len(steps) <= 6):
            raise serializers.ValidationError("Un chemin doit contenir entre 2 et 6 étapes.")

        for step in steps:
            if step['start_time'] >= step['end_time']:
                raise serializers.ValidationError(
                    "start_time doit être inférieur à end_time pour chaque étape."
                )
            if duration and step['end_time'] > duration:
                raise serializers.ValidationError(
                    "Une étape ne peut pas dépasser la durée totale de la vidéo."
                )

        return data

    @transaction.atomic
    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        gps_points_data = validated_data.pop('gps_points', [])
        user = self.context['request'].user

        # ✅ Récupérer l'établissement de l'utilisateur
        establishment = getattr(user, 'etablissement', None)

        path = Path.objects.create(
            user=user,
            establishment=establishment,
            status='draft',
            is_official=False,
            # ✅ Copier les champs de départ
            **validated_data
        )

        # ✅ Remplir les coordonnées de destination si l'établissement existe
        if establishment:
            path.end_lat = establishment.lat
            path.end_lng = establishment.lng
            path.save(update_fields=['end_lat', 'end_lng'])

        # Créer les étapes
        for step_data in steps_data:
            Step.objects.create(path=path, **step_data)

        # Créer les points GPS
        for index, gps_data in enumerate(gps_points_data):
            GPSPoint.objects.create(path=path, order=index, **gps_data)

        return path