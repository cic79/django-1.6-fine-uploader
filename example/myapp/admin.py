# !/usr/bin/env python
# encoding:UTF-8

import shutil

from django.contrib import admin
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import FileField
from django.forms import MultipleHiddenInput

from .models import FineFile


# TODO: fix the admin
# Class only used for denotation.


class FineFileAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.FileField: {
            'widget': MultipleHiddenInput(attrs={'admin': True, 'itemLimit': 1})
        },
    }

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
        )

    def fineuploader_setting(self, request):
        post_info = request.POST.dict()
        if type(self.formfield_overrides.get(FileField).get('widget')) is MultipleHiddenInput:
            model_fields = self.model._meta.fields
            file_fields_name = []
            for field in model_fields:
                if field.get_internal_type() is 'FileField':
                    file_fields_name.append(field.name)
            if request.method == 'POST':
                print(file_fields_name)
                for name in file_fields_name:
                    file_uploader = cache.get(request.POST.get(name))
                    if file_uploader is None:
                        return
                        # raise forms.ValidationError("There is no file in the field.")
                    file_path = file_uploader.storage.path(file_uploader.real_path)
                    post_info[name] = SimpleUploadedFile(
                        file_uploader.filename,
                        open(file_path, 'rb').read()
                    )
                    request.POST = post_info
                    folder_path = file_uploader.storage.path(file_uploader.file_path)
                    try:
                        shutil.rmtree(folder_path)
                    except OSError:
                        pass
        # return post_info

    def add_view(self, request, form_url='', extra_context=None):
        self.fineuploader_setting(request)
        return super(type(self), self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fineuploader_setting(request)
        return super(type(self), self).change_view(request, object_id, form_url, extra_context)


admin.site.register(FineFile, FineFileAdmin)
