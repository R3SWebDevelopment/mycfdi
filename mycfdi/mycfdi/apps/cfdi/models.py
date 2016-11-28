from django.db import models
from utils import *

CDFI_REQUIRED_FIELDS=[
    'version', 'sello', 'forma_de_pago' , 'no_certificado', 'certificado', 'tipo_de_comprobante', 'metodo_de_pago', 'lugar_expedicion',
]
CDFI_DEFINITION = [
    {
        'name': 'version',
        'class': 'str',
        'required': True,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'serie',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 1,
        'max': 25,
        'collapse_ws': True,
    },
    {
        'name': 'folio',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 1,
        'max': 20,
        'collapse_ws': True,
    },
    {
        'name': 'sello',
        'class': 'str',
        'required': True,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'forma_de_pago',
        'class': 'str',
        'required': True,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'no_certificado',
        'class': 'str',
        'required': True,
        'format': None,
        'min': 1,
        'max': 20,
        'collapse_ws': True,
    },
    {
        'name': 'certificado',
        'class': 'str',
        'required': True,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'condiciones_de_pago',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'motivo_descuento',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'tipo_cambio',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'metodo_de_pago',
        'class': 'str',
        'required': True,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
]

class CFDI(models.Model):
    ###String##################################################################
    version = models.TextField(default=None, null=True, blank=True)
    serie = models.TextField(default=None, null=True, blank=True)
    folio = models.TextField(default=None, null=True, blank=True)
    sello = models.TextField(default=None, null=True, blank=True)
    forma_de_pago = models.TextField(default=None, null=True, blank=True)
    no_certificado = models.TextField(default=None, null=True, blank=True)
    certificado = models.TextField(default=None, null=True, blank=True)
    condiciones_de_pago = models.TextField(default=None, null=True, blank=True)
    motivo_descuento = models.TextField(default=None, null=True, blank=True)
    tipo_cambio = models.TextField(default=None, null=True, blank=True)
    modena = models.TextField(default=None, null=True, blank=True)
    tipo_de_comprobante = models.TextField(default=None, null=True , blank=True)
    metodo_de_pago = models.TextField(default=None, null=True, blank=True)
    lugar_expedicion = models.TextField(default=None, null=True, blank=True)
    num_cta_pago = models.TextField(default=None, null=True, blank=True)
    folio_fiscal_orig = models.TextField(default=None, null=True, blank=True)

    @classmethod
    def fields(cls):
        fields = cls._meta.fields
        return fields

    @classmethod
    def required_fields(cls):
        return CDFI_REQUIRED_FIELDS

    @classmethod
    def is_required_field(cls, item):
        if cls.has_field(item) and item in cls.required_fields():
            return True
        return False

    @classmethod
    def has_field(cls, key=None):
        if key is not None and key in cls.fields():
            return True
        return False

    def __getattr__(self, item):
        value = None
        if self.__class__.has_field(key=item):
            if item is 'version':
                return self.version
        return value

    def __setattr__(self, key, value):
        if self.__class__.has_field(key=key):
            pass

