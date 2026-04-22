# from rest_framework import serializers
# from django.db import transaction
# from paths.models import Path, Step, GPSPoint, Establishment
# from paths.serializers.step_serializer import StepSerializer
# from paths.serializers.gps_serializer import GPSPointSerializer

# MAX_VIDEO_DURATION = 120


# class PathCreateSerializer(serializers.ModelSerializer):
#     steps = StepSerializer(many=True)
#     gps_points = GPSPointSerializer(many=True, required=False)
    
#     start_label = serializers.CharField(required=False, allow_blank=True)
#     end_label = serializers.CharField(required=False, allow_blank=True)  # ✅ AJOUTÉ
    
#     start_lat = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
#     start_lng = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    
#     end_lat = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
#     end_lng = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)

#     class Meta:
#         model = Path
#         fields = [
#             'id',
#             'title',
#             'start_label',
#             'end_label',  # ✅ AJOUTÉ
#             'start_lat',
#             'start_lng',
#             'end_lat',
#             'end_lng',
#             'video_url',
#             'duration',
#             'status',
#             'is_official',
#             'created_at',
#             'steps',
#             'gps_points',
#         ]
#         read_only_fields = ['status', 'is_official', 'created_at']

#     def validate_duration(self, value):
#         if value > MAX_VIDEO_DURATION:
#             raise serializers.ValidationError(
#                 f"La durée ne peut pas dépasser {MAX_VIDEO_DURATION} secondes."
#             )
#         if value <= 0:
#             raise serializers.ValidationError("La durée doit être supérieure à 0.")
#         return value

#     def validate(self, data):
#         steps = data.get('steps', [])
#         duration = data.get('duration')

#         if not (2 <= len(steps) <= 6):
#             raise serializers.ValidationError("Un chemin doit contenir entre 2 et 6 étapes.")

#         for step in steps:
#             if step['start_time'] >= step['end_time']:
#                 raise serializers.ValidationError("Le start_time doit être inférieur au end_time.")
#             if duration and step['end_time'] > duration:
#                 raise serializers.ValidationError("Une étape ne peut pas dépasser la durée totale.")

#         return data

#     @transaction.atomic
#     def create(self, validated_data):
#         steps_data = validated_data.pop('steps', [])
#         gps_points_data = validated_data.pop('gps_points', [])
#         validated_data.pop('user', None)

#         establishment = validated_data.pop('establishment', None)
#         user = self.context['request'].user

#         if not establishment:
#             establishment = getattr(user, 'etablissement', None)

#         # ✅ end_label automatique depuis le nom de l'établissement si non fourni
#         if not validated_data.get('end_label') and establishment:
#             validated_data['end_label'] = establishment.name

#         # ✅ Coordonnées envoyées par le mobile
#         mobile_end_lat = validated_data.get('end_lat')
#         mobile_end_lng = validated_data.get('end_lng')

#         path = Path.objects.create(
#             user=user,
#             establishment=establishment,
#             status='draft',
#             is_official=False,
#             **validated_data
#         )

#         # ✅ Fallback : coordonnées de l'établissement si mobile n'a pas envoyé
#         if (mobile_end_lat is None or mobile_end_lng is None) and establishment:
#             if establishment.lat and establishment.lng:
#                 path.end_lat = establishment.lat
#                 path.end_lng = establishment.lng
#                 path.save(update_fields=['end_lat', 'end_lng'])

#         for step_data in steps_data:
#             Step.objects.create(path=path, **step_data)

#         for index, gps_data in enumerate(gps_points_data):
#             GPSPoint.objects.create(path=path, order=index, **gps_data)

#         return path
from rest_framework import serializers
from django.db import transaction
from paths.models import Path, Step, GPSPoint, Establishment
from paths.serializers.step_serializer import StepSerializer
from paths.serializers.gps_serializer import GPSPointSerializer

MAX_VIDEO_DURATION = 120


class PathCreateSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    gps_points = GPSPointSerializer(many=True, required=False)
    
    start_label = serializers.CharField(required=False, allow_blank=True)
    end_label = serializers.CharField(required=False, allow_blank=True)
    
    start_lat = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    start_lng = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    
    end_lat = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    end_lng = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)

    # ✅ AJOUT — champ platform optionnel, défaut 'mobile' pour ne pas casser l'app mobile
    platform = serializers.ChoiceField(
        choices=['mobile', 'web'],
        required=False,
        default='mobile'
    )
    # ✅ AJOUT — establishment_id optionnel pour la version web (admin panel)
    establishment_id = serializers.IntegerField(required=False, allow_null=True)


    class Meta:
        model = Path
        fields = [
            'id',
            'title',
            'start_label',
            'end_label',
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
            # ✅ AJOUT
            'platform',
            'establishment_id',
        ]
        read_only_fields = ['status', 'is_official', 'created_at']

    def validate_duration(self, value):
        if value > MAX_VIDEO_DURATION:
            raise serializers.ValidationError(
                f"La durée ne peut pas dépasser {MAX_VIDEO_DURATION} secondes."
            )
        if value <= 0:
            raise serializers.ValidationError("La durée doit être supérieure à 0.")
        return value

    def validate(self, data):
        steps = data.get('steps', [])
        duration = data.get('duration')

        if not (2 <= len(steps) <= 6):
            raise serializers.ValidationError("Un chemin doit contenir entre 2 et 6 étapes.")

        for step in steps:
            if step['start_time'] >= step['end_time']:
                raise serializers.ValidationError("Le start_time doit être inférieur au end_time.")
            if duration and step['end_time'] > duration:
                raise serializers.ValidationError("Une étape ne peut pas dépasser la durée totale.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        gps_points_data = validated_data.pop('gps_points', [])
        validated_data.pop('user', None)

        # ✅ AJOUT — récupère platform (mobile par défaut, ne casse pas l'app mobile)
        platform = validated_data.pop('platform', 'mobile')

        # ✅ AJOUT — récupère establishment_id si envoyé (depuis version web)
        establishment_id = validated_data.pop('establishment_id', None)

        user = self.context['request'].user

        # ✅ MODIFIÉ — cherche l'établissement par establishment_id (web)
        # ou par le compte utilisateur (mobile/établissement) — ordre de priorité :
        # 1. establishment_id explicite (envoyé par le panel admin ou la version web)
        # 2. établissement lié au compte utilisateur (mobile établissement)
        establishment = validated_data.pop('establishment', None)
    
        if not establishment:
            establishment = getattr(user, 'etablissement', None)

        # ✅ end_label automatique depuis le nom de l'établissement si non fourni
        if not validated_data.get('end_label') and establishment:
            validated_data['end_label'] = establishment.name

        # ✅ Coordonnées envoyées par le mobile
        mobile_end_lat = validated_data.get('end_lat')
        mobile_end_lng = validated_data.get('end_lng')

        # ✅ Statut et is_official selon le rôle de l'utilisateur
        is_trusted = user.is_staff or user.is_superuser or (establishment is not None)
        status = 'published' if is_trusted else 'draft'
        is_official = is_trusted

        path = Path.objects.create(
            user=user,
            establishment=establishment,
            status=status,
            is_official=is_official,
            platform=platform,#Ajout✅
            **validated_data
        )

        # ✅ Fallback : coordonnées de l'établissement si mobile n'a pas envoyé
        if (mobile_end_lat is None or mobile_end_lng is None) and establishment:
            if establishment.lat and establishment.lng:
                path.end_lat = establishment.lat
                path.end_lng = establishment.lng
                path.save(update_fields=['end_lat', 'end_lng'])

        for step_data in steps_data:
            Step.objects.create(path=path, **step_data)

        for index, gps_data in enumerate(gps_points_data):
            GPSPoint.objects.create(path=path, order=index, **gps_data)

        return path