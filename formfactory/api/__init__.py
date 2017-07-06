from rest_framework import viewsets
from rest_framework import serializers

import rest_framework_extras

from formfactory.models import Form, FormFieldGroup


class FieldGroupRelatedMixin(serializers.Serializer):
    fields = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="formfield-detail"
    )

    class Meta(object):
        fields = ("fields", )


class FormRelatedMixin(serializers.Serializer):
    fieldgroups = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="formfieldgroup-detail"
    )

    class Meta(object):
        fields = ("fieldgroups", )


class PropertiesMixin(serializers.Serializer):
    absolute_url = serializers.ReadOnlyField()

    class Meta(object):
        fields = ("absolute_url", )


class FieldGroupSerializer(
        FieldGroupRelatedMixin, serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = FormFieldGroup


class FieldGroupObjectsViewSet(viewsets.ModelViewSet):
    queryset = FormFieldGroup.objects.all()
    serializer_class = FieldGroupSerializer


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
            ("formfactory-formfieldgroup", FieldGroupObjectsViewSet),
        )
    )
