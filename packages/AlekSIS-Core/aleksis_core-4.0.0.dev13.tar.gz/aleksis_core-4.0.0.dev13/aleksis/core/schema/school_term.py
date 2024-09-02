from django.core.exceptions import PermissionDenied

from graphene_django import DjangoObjectType

from ..models import SchoolTerm
from .base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    PermissionsTypeMixin,
)


class SchoolTermType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = SchoolTerm
        filter_fields = {
            "name": ["icontains", "exact"],
            "date_start": ["exact", "lt", "lte", "gt", "gte"],
            "date_end": ["exact", "lt", "lte", "gt", "gte"],
        }
        fields = ("id", "name", "date_start", "date_end")

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        if not info.context.user.has_perm("core.view_schoolterm_rule"):
            raise PermissionDenied

        return queryset


class SchoolTermBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = SchoolTerm
        permissions = ("core.create_schoolterm_rule",)
        only_fields = ("id", "name", "date_start", "date_end")


class SchoolTermBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = SchoolTerm
        permissions = ("core.delete_schoolterm_rule",)


class SchoolTermBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = SchoolTerm
        permissions = ("core.edit_schoolterm_rule",)
        only_fields = ("id", "name", "date_start", "date_end")
