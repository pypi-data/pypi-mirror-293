from django.contrib import admin


class SummaryAdmin(admin.ModelAdmin):
    change_list_template = 'django_summary_admin/summary_change_list.html'

    def get_summary(self, queryset):
        return None

    def changelist_view(self, request, extra_context=None):
        view = super().changelist_view(request, extra_context)
        try:
            view.context_data['summary'] = self.get_summary(view.context_data['cl'].queryset)
        except KeyError:
            pass
        except AttributeError:
            pass
        return view


class LinksAdmin(admin.ModelAdmin):
    change_form_template = 'change_links/change_form.html'

    def get_links(self, obj):
        return None

    def change_view(self, request, object_id, form_url="", extra_context=None):
        view = super().change_view(request, object_id, form_url, extra_context)
        if not object_id:
            return view
        try:
            view.context_data['links'] = self.get_links(view.context_data['original'])
        except KeyError:
            pass
        except AttributeError:
            pass
        return view