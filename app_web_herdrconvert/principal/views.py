from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.views.generic.edit import FormView
from django.conf import settings
from .upload.forms import FileFieldForm
from .herdr_geojson import merge_to_geojson
import json
import os
import base64
# Create your views here.


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'principal/index.html'  # Replace with your template.
    # success_url = '/'  # Replace with your URL or reverse().
    success_url = reverse_lazy("index_listgeojson", kwargs={'key': 'file_updated_yes'}) 

    def handle_uploaded_file(self, f):  
        with open(settings.MEDIA_ROOT +"/" + f.name, 'wb+') as destination:  
            i = 0
            for chunk in f.chunks():
                print(i, "====>", chunk)
                destination.write(chunk)  
                i += 1

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            
            points_feature_collection, polylines_feature_collection = merge_to_geojson.convert_form_list(files)
            request.session["points_fc"] = points_feature_collection
            request.session["polylines_fc"] = polylines_feature_collection
            # for file_i in files:
            #     self.handle_uploaded_file(file_i)
            # merge_to_geojson.convert()
            c1 = "cd " + settings.MEDIA_ROOT
            c2 = 'rm -v !("points.geojson"|"polylines.geojson")'
            c_rm = 'rm ' + settings.MEDIA_ROOT +'/* -v !("points.geojson"|"polylines.geojson")'
            c = "(" + c1 + ";" + c2 + ")"
            print(c)
            os.system(c1)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                             
        points_fc = self.request.session.get("points_fc")
        polylines_fc = self.request.session.get("polylines_fc")
        points_fc = json.dumps(points_fc)
        polylines_fc = json.dumps(polylines_fc)
        # print(points_fc, polylines_fc)

        context["points_fc"] = points_fc
        context["polylines_fc"] = polylines_fc
        context["file_updated"] = self.kwargs.get("key", None)
        context["query_params"] = self.request.GET.get("q", "a default") # should be testingtesting
        return context

# https://dorbae.github.io/python/django/python-django-downloadfile/
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/geojson")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    
    # if request.method == 'POST':
        # var = request.FILES.get
    var = "ok"
    return render(
        request, 'principal/index.html',
        {"test": var}
    )
## Oauth pour recupperer
## cozy cloud log par oAuth, login button
## user accounts pour l'application
## supprimer ou garder les fichiers dans un drive(OAuth)
## UI avec Charlotte, proposer à Vincent
## Deploy sur Heroku
## Mail a Vincent

## App web avec Javascript pour le filtrage des datas
## Express JS,
## compte users, tokkent pour notre service --> va dans la carte
## Dashboard creer un nouveau compte, pour utiliser le filtrage, juste pour intepreter les datas de la ville (JALON)
## 