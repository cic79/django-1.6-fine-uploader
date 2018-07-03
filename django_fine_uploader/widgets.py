import json

from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class FineUploaderWidget(forms.MultipleHiddenInput):
    template_name = 'django_fine_uploader/widget.html'

    def __init__(self, attrs=None, **kwargs):
        self.attrs = attrs or {}
        self.options = kwargs.pop('options', {})

        self.allow_delete = kwargs.pop('allow_delete', True)
        self.allow_retry = kwargs.pop('allow_retry', True)
        self.drop_label = kwargs.get('drop_label', _('Or just drag and drop file(s) here'))
        self.upload_label = kwargs.get('upload_label', _('Select file(s)'))
        self.delete_label = kwargs.pop('delete_label', _('Delete'))
        self.retry_label = kwargs.pop('retry_label', _('Retry'))
        self.pause_label = kwargs.pop('pause_label', _('Pause'))
        self.continue_label = kwargs.pop('continue_label', _('Continue'))
        self.close_label = kwargs.get('close_label', _('Close'))
        self.yes_label = kwargs.get('yes_label', _('Yes'))
        self.no_label = kwargs.get('no_label', _('No'))
        self.ok_label = kwargs.get('ok_label', _('OK'))
        self.cancel_label = kwargs.get('cancel_label', _('Cancel'))

        self.include_js = kwargs.pop('include_js', True)
        self.include_css = kwargs.pop('include_css', True)

        self.itemLimit = self.attrs.get('itemLimit', 0)
        self.admin = self.attrs.get('admin', False)
        if self.admin:
            self.input_type = ''
        super(FineUploaderWidget, self).__init__(attrs, **kwargs)
        self.type = 'hidden'

    def get_context(self, name, value, attrs):
        if self.admin:
            value = None
        context = super(FineUploaderWidget, self).get_context(name, value, attrs)
        upload_url = reverse('django_fine_uploader:upload')
        options = {
            'request': {
                'params': {
                    'qqadmin': self.admin,
                },
                'endpoint': upload_url,
            },
            'deleteFile': {
                'enabled': True,
                'endpoint': reverse('django_fine_uploader:delete'),
            },
            'chunking': {
                'enabled': True,
                'concurrent': {
                    'enabled': True
                },
                'success': {
                    'endpoint': '%s?done' % upload_url
                }
            },
            'validation': {
                'itemLimit': self.itemLimit
            }
        }

        options.update(self.options)
        context['widget'].update({
            'options': json.dumps(options),
            'allow_delete': self.allow_delete,
            'allow_retry': self.allow_retry,
            'drop_label': self.drop_label,
            'upload_label': self.upload_label,
            'delete_label': self.delete_label,
            'retry_label': self.retry_label,
            'pause_label': self.pause_label,
            'continue_label': self.continue_label,
            'close_label': self.close_label,
            'yes_label': self.yes_label,
            'no_label': self.no_label,
            'ok_label': self.ok_label,
            'cancel_label': self.cancel_label,
            'admin': json.dumps(self.admin),
        })
        return context

    @property
    def media(self):
        kwargs = {}
        if self.include_js:
            kwargs['js'] = (
                'django_fine_uploader/js-cookie/js.cookie.min.js',
                'django_fine_uploader/fine-uploader.min.js',
            )
        if self.include_css:
            kwargs['css'] = {
                'all': ('django_fine_uploader/fine-uploader-gallery.min.css',)
            }
        return forms.Media(**kwargs)
