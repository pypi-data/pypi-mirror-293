from typing import Iterable

from django.contrib import admin, messages
from django.forms import Form
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html


class ActionButton:
    def __init__(
        self,
        name: str,
        url_name: str = None,
        form: Form = None,
        admin_function: str = None,
        model_function: str = None,
        color: str = "#264b5d",
        url: str = None,
    ):
        self.name = name
        self.form = form
        self.color = color

        if (admin_function and model_function) or (
            not admin_function and not model_function
        ):
            raise Exception("Either admin_function or model_function must provide")

        self.admin_function = admin_function
        self.model_function = model_function

        if url:
            self.url = url
        else:
            self.url = (
                self.admin_function if self.admin_function else self.model_function
            )

        if url_name:
            self.url_name = url_name
        else:
            self.url_name = self.url

    @property
    def permission_name(self) -> str:
        return f"admin action button | {self.name}"

    @property
    def permission_codename(self) -> str:
        return f"admin_action_button_{self.url}"


class ActionButtonAdmin(admin.ModelAdmin):
    action_buttons: Iterable[ActionButton] = ()

    def handle_action_button(self, request, *args, **kwargs):
        admin_function = kwargs.get("admin_function")
        model_function = kwargs.get("model_function")
        permission_codename = kwargs.get("permission_codename")
        object_id = kwargs.get("object_id")

        if not request.user.has_perm(permission_codename) and not request.user.is_superuser:
            self.message_user(
                request=request,
                message="This action is not allowed",
                level=messages.ERROR,
            )

        elif admin_function:
            return getattr(self, admin_function)(request, *args, **kwargs)

        elif model_function:
            try:
                obj = self.get_object(request=request, object_id=object_id)
                getattr(obj, model_function)()

                self.message_user(
                    request=request, message="Action done!", level=messages.SUCCESS
                )

            except Exception as e:
                self.message_user(
                    request=request,
                    message=f"{e.__class__.__name__}: {str(e)}",
                    level=messages.ERROR,
                )

        else:
            raise Exception("No function provided")

        url = reverse(
            f"admin:{self.opts.app_label}_{self.opts.model_name}_change",
            args=[object_id],
            current_app=self.admin_site.name,
        )

        return HttpResponseRedirect(url)

    @admin.action(description="Action")
    def render_action_button(self, obj):
        action_button_tags = ""

        for action in self.action_buttons:
            admin_url_name = (
                f"admin:{self.opts.app_label}_{self.opts.model_name}_{action.url_name}"
            )
            action_button_tags += f"&nbsp;<a class='button' style='background-color: {action.color}; white-space: nowrap;' href='{reverse(admin_url_name, args=[obj.pk])}'>{action.name}</a>"

        return format_html(action_button_tags)

    render_action_button.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))

        if self.action_buttons:
            readonly_fields.append("render_action_button")

        return readonly_fields

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))

        if self.action_buttons:
            list_display.insert(1, "render_action_button")

        return list_display

    def get_urls(self):
        urls = super().get_urls()
        action_urls = []

        for action in self.action_buttons:
            action_urls.append(
                path(
                    f"<path:object_id>/{action.url}/",
                    self.handle_action_button,
                    name=f"{self.opts.app_label}_{self.opts.model_name}_{action.url_name}",
                    kwargs={
                        "admin_function": action.admin_function,
                        "model_function": action.model_function,
                        "permission_codename": action.permission_codename,
                    },
                ),
            )

        return action_urls + urls
