from django.db import models
from utils import *
import uuid

CDFI_REQUIRED_FIELDS=[
    'version', 'sello', 'forma_de_pago' , 'no_certificado', 'certificado', 'tipo_de_comprobante', 'metodo_de_pago', 'lugar_expedicion', 'fecha', 'fecha_folio_fiscal_orig', 'subtotal', 'total'
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
    {
        'name': 'lugar_expedicion',
        'class': 'str',
        'required': True,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'num_cta_pago',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 4,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'folio_fiscal_orig',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'serie_folio_fiscal_orig',
        'class': 'str',
        'required': False,
        'format': None,
        'min': 1,
        'max': None,
        'collapse_ws': True,
    },
    {
        'name': 'fecha',
        'class': 'datetime',
        'required': True,
        'format': 'yyyy-mm-ddThh:mm:ss',
    },
    {
        'name': 'fecha_folio_fiscal_orig',
        'class': 'datetime',
        'required': False,
        'format': 'yyyy-mm-ddThh:mm:ss',
    },
    {
        'name': 'subtotal',
        'class': 'decimal',
        'required': True,
    },
    {
        'name': 'descuento',
        'class': 'decimal',
        'required': False,
    },
    {
        'name': 'total',
        'class': 'decimal',
        'required': True,
    },
    {
        'name': 'monto_folio_fiscal_orig',
        'class': 'decimal',
        'required': False,
    },
]

class Base(models.Model):
    ###Internal Control########################################################
    uuid = models.UUIDField(editable=False, null=False, blank=False, default=uuid.uuid4())
    active = models.NullBooleanField(default=True)
    valid = models.NullBooleanField(default=False)
    validation_feedback = models.TextField(default=None, null=True, blank=True)
    data = models.TextField(null=False, blank=False)

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

class RegimenFiscal(models.Model):
    ###String##################################################################
    regimen = models.TextField(default=None, null=True, blank=True)

class Domicilio(Base):
    ###String##################################################################
    calle = models.TextField(default=None, null=True, blank=True)
    no_exterior = models.TextField(default=None, null=True, blank=True)
    no_interior = models.TextField(default=None, null=True, blank=True)
    colonia = models.TextField(default=None, null=True, blank=True)
    localidad = models.TextField(default=None, null=True, blank=True)
    referencia = models.TextField(default=None, null=True, blank=True)
    municipio = models.TextField(default=None, null=True, blank=True)
    estado = models.TextField(default=None, null=True, blank=True)
    pais = models.TextField(default=None, null=True, blank=True)
    codigo_postal = models.TextField(default=None, null=True, blank=True)

class PersonaFiscal(Base):
    ###String##################################################################
    rfc = models.TextField(default=None, null=True, blank=True)
    nombre = models.TextField(default=None, null=True, blank=True)
    ###ForeignKey##################################################################
    domicilio_relation = models.ForeignKey('Domicilio', blank=False, null=False, related_name='cfdi_domicilio')

class Receptor(PersonaFiscal):
    pass

class Emisor(PersonaFiscal):
    ###ForeignKey##################################################################
    expedido_en_relation = models.ForeignKey('Domicilio', blank=False, null=False, related_name='cfdi_expedido')
    ###ManyToMany##################################################################
    regimen_fiscal_relations = models.ManyToManyField('RegimenFiscal')

class InformacionAduanera(Base):
    ###String##################################################################
    numero = models.TextField(default=None, null=True, blank=True)
    aduana = models.TextField(default=None, null=True, blank=True)
    ###DateTime##################################################################
    fecha = models.DateField(default=None, null=True, blank=True)

class ConceptoPredial(models.Model):
    ###String##################################################################
    numero = models.TextField(default=None, null=True, blank=True)

class Parte(Base):
    ###String##################################################################
    unidad = models.TextField(default=None, null=True, blank=True)
    no_identificacion = models.TextField(default=None, null=True, blank=True)
    descripcion = models.TextField(default=None, null=True, blank=True)
    ###Decimal##################################################################
    cantidad = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    valor_unitario = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    importe = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    ###ManyToMany##################################################################
    informacion_aduanera_relations = models.ManyToManyField('InformacionAduanera')

class Concepto(Base):
    ###String##################################################################
    unidad = models.TextField(default=None, null=True, blank=True)
    no_identificacion = models.TextField(default=None, null=True, blank=True)
    descripcion = models.TextField(default=None, null=True, blank=True)
    ###Decimal##################################################################
    cantidad = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    valor_unitario = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    importe = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    ###ForeignKey##################################################################
    predial_relation = models.ForeignKey('ConceptoPredial' , blank=False, null=False, related_name='concepto')
    ###ManyToMany##################################################################
    informacion_aduanera_relations = models.ManyToManyField('InformacionAduanera')
    partes_relations = models.ManyToManyField('Parte')
    complementos_relations = models.ManyToManyField('Concepto')

class ImpuestosAplicaciones(models.Model):
    ###Decimal##################################################################
    impuesto = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    importe = models.DecimalField(default=None, max_digits=8, decimal_places=2)

class Retenidos(ImpuestosAplicaciones):
    pass

class Trasladado(ImpuestosAplicaciones):
    ###Decimal##################################################################
    tasa = models.DecimalField(default=None, max_digits=8, decimal_places=2)

class Impuesto(Base):
    ###Decimal##################################################################
    total_impuestos_retenidos = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    total_impuestos_trasladados = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    ###ManyToMany##################################################################
    retenidos_relations = models.ManyToManyField('Retenidos', related_name='impuesto_retenidos')
    trasladados_relations = models.ManyToManyField('Trasladado', related_name='impuesto_transladados')

class Complemento(models.Model):
    ###String##################################################################
    lead = models.TextField(default=None, null=True, blank=True)
    key = models.TextField(default=None, null=True, blank=True)
    value = models.TextField(default=None, null=True, blank=True)

class Addenda(models.Model):
    ###String##################################################################
    lead = models.TextField(default=None, null=True, blank=True)
    key = models.TextField(default=None, null=True, blank=True)
    value = models.TextField(default=None, null=True, blank=True)

class CFDI(Base):
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
    serie_folio_fiscal_orig = models.TextField(default=None, null=True, blank=True)
    ###DateTime##################################################################
    fecha = models.DateTimeField(default=None, null=True, blank=True)
    fecha_folio_fiscal_orig = models.DateTimeField(default=None, null=True, blank=True)
    ###Decimal##################################################################
    subtotal = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    descuento = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    total= models.DecimalField(default=None, max_digits=8, decimal_places=2)
    monto_folio_fiscal_orig = models.DecimalField(default=None, max_digits=8, decimal_places=2)
    ###ForeignKey##################################################################
    emisor_relation = models.ForeignKey('Emisor' , blank=False, null=False, related_name='cfdi_emitidas')
    receptor_relation = models.ForeignKey('Receptor' , blank=False, null=False, related_name='cfdi_recibidas')
#    complemento_relation = models.ForeignKey('Complemento' , blank=False, null=False, related_name='cfdi_complemento')
#    addenda_relation = models.ForeignKey('Addenda' , blank=False, null=False, related_name='cfdi_addenda')
    ###ManyToMany##################################################################
    conceptos_relations = models.ManyToManyField('Concepto')
    impuestos_relations = models.ManyToManyField('Impuesto')
    complementos_relations = models.ManyToManyField('Complemento')
    addenda_relations = models.ManyToManyField('Addenda')

class CFDIXML(models.Model):
    processed = models.NullBooleanField(default=False)
    xml_file = models.FileField(upload_to="cfdi/")
    data = models.TextField(null=True, blank=True)
    md5 = models.TextField(null=False, blank=False)
    sha1 = models.TextField(null=False, blank=False)
    ###ForeignKey##################################################################
    cfdi = models.ForeignKey('CFDI', blank=True, null=True, related_name='xml')

    @classmethod
    def add(cls, file=None):
        instance = None
        md5, sha1 = hash_file(file=file)
        if md5 is not None and sha1 is not None:
            try:
                md5 = "{0}".format(md5.hexdigest())
                sha1 = "{0}".format(sha1.hexdigest())
            except:
                md5 = None
                sha1 = None
            if md5 is not None and md5.strip() and sha1 is not None and sha1.strip():
                if not cls.objects.filter(md5__iexact=md5).filter(sha1__iexact=sha1).exists():
                    instance = cls.objects.create(md5 = md5, sha1 = sha1)
                    if instance is not None:
                        try:
                            instance.xml_file.save(file.name, file)
                        except:
                            pass
                else:
                    instance = cls.objects.filter(md5__iexact=md5).filter(sha1__iexact=sha1).first()
        return instance