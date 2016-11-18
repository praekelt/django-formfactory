from rest_framework import viewsets
from rest_framework import serializers

import rest_framework_extras

from formfactory.models import Form, FormField


class FormRelatedMixin(serializers.Serializer):
    fields = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="formfield-detail"
    )

    class Meta(object):
        fields = ("fields", )


class PropertiesMixin(serializers.Serializer):
    absolute_url = serializers.ReadOnlyField()

    class Meta(object):
        fields = ("absolute_url", )


class FormSerializer(
        PropertiesMixin, FormRelatedMixin,
        serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = Form


class FormObjectsViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer


def register(router):
    return rest_framework_extras.register(
        router, (
            ("formfactory-form", FormObjectsViewSet),
        )
    )
