from django.conf.urls import url
from rest_views import *

urlpatterns = [
    url(r'xml/upload/$' , upload_xml_cfdi , name='upload_xml_cfdi') ,
    url(r'view/(?P<uuid>\w+)/$' , cfdi_view , name='cfdi_view') ,
]