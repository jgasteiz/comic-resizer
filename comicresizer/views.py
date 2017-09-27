from wsgiref.util import FileWrapper

from django.http import HttpResponse, StreamingHttpResponse
from django.views.generic.edit import FormView

from .forms import ComicUploadForm
from .utils import resize_comic


class ResizeComicView(FormView):
    form_class = ComicUploadForm
    template_name = 'comicresizer/index.html'

    def form_valid(self, form):
        file = form.cleaned_data.get('file')
        resized_comic = resize_comic(file)

        response = StreamingHttpResponse(FileWrapper(resized_comic), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.name)
        response['Content-Length'] = resized_comic.tell()

        resized_comic.seek(0)

        return response


resize_comic_view = ResizeComicView.as_view()
