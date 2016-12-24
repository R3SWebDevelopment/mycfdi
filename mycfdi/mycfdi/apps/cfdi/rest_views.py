from mycfdi.lib.decorators import render
from django.views.decorators.http import require_http_methods
from django.utils.datastructures import MultiValueDict
from models import *

def REST(template = None , content_type = 'json' , **kwargs):
	path = 'cfdi'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

@require_http_methods(["POST"])
@REST(template="")
def upload_xml_cfdi(request):
    if request.FILES is not None and request.FILES.__class__ is MultiValueDict:
        FILES = request.FILES.getlist('uploadedFile')
    else:
        FILES = []
    for file in FILES:
        instance = CFDIXML.add(file=file)
        print "instance: %s" % instance
    return{}

@REST(template="")
def cfdi_view(request , uuid=None):
    json_data = None
    if uuid is not None and uuid.strip():
        cfdi = CFDI.objects.filter(uuid = uuid).first()
        if cfdi is not None:
            json_data = cfdi.rest_data
    return{
        'response_data' : json_data,
    }