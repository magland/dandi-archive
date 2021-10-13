from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef, Q
from django.http.response import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView

from dandiapi.api.models import Asset, AssetBlob, Upload, Version
from dandiapi.api.views.users import social_account_to_dict


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context['orphaned_asset_count'] = self._orphaned_asset_count()
        context['orphaned_asset_blob_count'] = self._orphaned_asset_blob_count()
        non_valid_assets = self._non_valid_assets()
        context['non_valid_asset_count'] = non_valid_assets.count()
        context['non_valid_assets'] = non_valid_assets[:10]
        uploads = self._uploads()
        context['upload_count'] = uploads.count()
        context['uploads'] = uploads[:10]

        return context

    def _orphaned_asset_count(self):
        return (
            Asset.objects.annotate(
                has_version=Exists(Version.objects.filter(assets=OuterRef('id')))
            )
            .filter(has_version=False)
            .count()
        )

    def _orphaned_asset_blob_count(self):
        return (
            AssetBlob.objects.annotate(
                has_asset=Exists(Asset.objects.filter(blob_id=OuterRef('id')))
            )
            .filter(has_asset=False)
            .count()
        )

    def _non_valid_assets(self):
        return (
            Asset.objects.annotate(
                has_version=Exists(Version.objects.filter(assets=OuterRef('id')))
            )
            .filter(has_version=True)
            .filter(~Q(status=Asset.Status.VALID))
        )

    def _uploads(self):
        return Upload.objects.annotate()


@require_http_methods(['GET', 'POST'])
def user_approval_view(request, username: str):
    if not request.user.is_superuser:
        raise PermissionDenied()

    user = User.objects.filter(username=username).select_related('metadata').first()

    if user is None:
        raise Http404('User not found')

    if request.method == 'POST':
        req_body = request.POST.dict()
        user.metadata.status = req_body.get('status')
        if req_body.get('rejection_reason') is not None:
            user.metadata.rejection_reason = req_body.get('rejection_reason')
        user.metadata.save()

    social_account = user.socialaccount_set.first()

    return render(
        request,
        'dashboard/user_approval.html',
        {
            'user': user,
            'social_account': social_account_to_dict(social_account)
            if social_account is not None
            else None,
        },
    )
