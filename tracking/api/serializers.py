"""
Serializer for the tracking app
"""
from rest_framework import serializers

from tracking.models import Contract, Project, Timelog
from users.models import User


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project
    """

    class Meta:
        model = Project
        fields = ('id', 'name')


class ContractReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading a contract
    """

    project = ProjectSerializer()

    class Meta:
        model = Contract
        fields = ('id', 'user', 'project', 'hourly_price')


class ContractWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for the writing a Contract
    """

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contract
        fields = ('user', 'project', 'hourly_price',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'project'),
                message='Contract already exists for the given user and project'
            )
        ]

    def create(self, validated_data):
        """
        Create a contract with the given user_id and project_id
        """

        request = self.context.get('request')

        if not request.user.is_staff and (request.user.id != validated_data['user'].id):
            raise serializers.ValidationError({'user': 'You do not have permission for this'})

        return Contract.objects.create(
            project=validated_data['project'],
            user=validated_data['user'],
            hourly_price=validated_data['hourly_price']
        )


class TimelogWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for the writing a Timelog
    """

    class Meta:
        model = Timelog
        fields = ('date', 'contract', 'hours_worked')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('contract', 'date'),
                message='Log for this contract already exists for the given date'
            )
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        user_contracts = Contract.objects.filter(user=request.user)
        self.fields['contract'] = serializers.PrimaryKeyRelatedField(
            required=True,
            queryset=user_contracts
        )


class TimelogReadSerializer(serializers.ModelSerializer):
    """
    Serializer for the displaying a Timelog
    """

    contract = ContractReadSerializer()

    class Meta:
        model = Timelog
        fields = ('id', 'date', 'hours_worked', 'contract')
