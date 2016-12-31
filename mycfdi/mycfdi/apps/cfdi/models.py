from django.db import models
from utils import *
from uuid import uuid4
from bs4 import BeautifulSoup
from shortuuidfield import ShortUUIDField
from datetime import datetime


CFDI_COMPROBANTE_DEFINITION=retrive_definition(component = 'json/cfdi/comprobante.json')
CFDI_TIMBRE_FISCAL_DIGITAL_DEFINITION=retrive_definition(component = 'json/cfdi/timbre_fiscal_digital.json')
CFDI_PERSONA_FISICAL_DEFINITION=retrive_definition(component ='json/cfdi/persona_fiscal.json')
CFDI_DOMICILIO_DEFINITION=retrive_definition(component = 'json/cfdi/domicilio.json')
CFDI_REGIMEN_FISCAL_DEFINITION=retrive_definition(component = 'json/cfdi/regimen_fiscal.json')
CFDI_CONCEPTO_DEFINITION=retrive_definition(component = 'json/cfdi/concepto.json')
CFDI_IMPUESTO_DEFINITION=retrive_definition(component = 'json/cfdi/impuesto.json')
CFDI_TRASLADADO_DEFINITION=retrive_definition(component = 'json/cfdi/trasladado.json')
CFDI_RETENIDO_DEFINITION=retrive_definition(component = 'json/cfdi/retenido.json')

class Base(models.Model):
    ###Internal Control########################################################
##    uuid = models.UUIDField(editable=False, null=False, blank=False, default=uuid4())
    uuid = ShortUUIDField(max_length=255, db_index=False)
    active = models.NullBooleanField(default=True)
    valid = models.NullBooleanField(default=False)
    validation_feedback = models.TextField(default=None, null=True, blank=True)
    data = models.TextField(null=False, blank=False)

    @classmethod
    def get_definition(cls):
        return {}

    @classmethod
    def get_attributes(cls):
        attributes = []
        definition = cls.get_definition()
        if definition is not None and definition.__class__ is dict:
            if 'attributes' in definition.keys():
                attributes = definition.get('attributes') or []
        return attributes

    @classmethod
    def get_required_attributes(cls):
        attributes = []
        for attr in cls.get_attributes():
            if 'required' in attr.keys() and attr.get('required') is True:
                attributes.append(attr)
        return attributes

    @classmethod
    def get_fields_keys(cls):
        return [
            {
                'key' : attr.get('key') ,
                'field': attr.get('name'),
            } for attr in cls.get_attributes() if 'name' in attr.keys() and attr.get('name') is not None and 'key' in attr.keys() and attr.get('key') is not None
        ]

    @classmethod
    def get_fields(cls):
        fields = [ attr.get('name') for attr in cls.get_attributes() if 'name' in attr.keys() and attr.get('name') is not None ]
        return fields

    @classmethod
    def get_required_fields(cls):
        fields = [ attr.get('name') for attr in cls.get_required_attributes() if 'name' in attr.keys() and attr.get('name') is not None ]
        return fields

    @classmethod
    def get_keys(cls):
        fields = [ attr.get('key') for attr in cls.get_attributes() if 'key' in attr.keys() and attr.get('key') is not None ]
        return fields

    @classmethod
    def get_required_keys(cls):
        fields = [ attr.get('key') for attr in cls.get_required_attributes() if 'key' in attr.keys() and attr.get('key') is not None ]
        return fields

    @classmethod
    def is_required_field(cls, item):
        if cls.has_field(item) and item in cls.get_required_fields():
            return True
        return False

    @classmethod
    def has_field(cls, key=None):
        if key is not None and key in cls.fields():
            return True
        return False

    @classmethod
    def fields(cls):
        fields = cls._meta.fields
        return fields

    @classmethod
    def decode(cls, data = None):
        d = {}
        if data is not None:
            for attr in cls.get_fields_keys():
                key = attr.get('key') or None
                field = attr.get('field') or None
                if key is not None and key.strip() and field is not None and field.strip():
                    value = None
                    if data.has_attr(key):
                        value = data.get(key) or None
                    d.update({
                        field : value
                    })
        return d

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

    def push_attributes(self, attributes = {}):
        if attributes is not None and attributes.__class__ is dict:
            for key in attributes.keys():
                value = attributes.get(key) or None
                setattr(self, key, value)
                self.save()

    @classmethod
    def get_serializer(cls):
        return None

    @classmethod
    def filtering(cls, data=None , filtering={}):

        return data

    @classmethod
    def rest_list(cls, **kwargs):
        rest_list = []
        serialiser = cls.get_serializer()
        if serialiser is not None:
            if 'filtering' in kwargs.keys():
                filtering = kwargs.get('filtering') or {}
            else:
                filtering = {}
            if 'data' in kwargs.keys():
                data = kwargs.get('data') or None
            if data is None:
                data = cls.objects.all()
            data = cls.filtering(data = data , filtering=filtering)
            serialized = serialiser(data, many=True)
            rest_list = serialized.data or None
        return rest_list

    @property
    def rest_data(self):
        serialiser = self.__class__.get_serializer()
        if serialiser is not None:
            serialized = serialiser(self)
            return serialized.data or None
        return None

class RegimenFiscal(Base):
    ###String##################################################################
    regimen = models.TextField(default=None, null=True, blank=True)

    @classmethod
    def get_definition(cls):
        return CFDI_REGIMEN_FISCAL_DEFINITION or {}

    @classmethod
    def add(cls, data=None):
        instance = None
        if data is not None and data.strip():
            soup = BeautifulSoup(data, 'xml')
            regimen_fiscal = soup.find('REGIMENFISCAL')
            if regimen_fiscal is not None:
                attributes = cls.decode(data=regimen_fiscal)
                instance = cls.objects.create()
                if instance is not None:
                    instance.push_attributes(attributes=attributes)
        return instance

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

    @classmethod
    def get_serializer(cls):
        from serializers import DomicilioSerializer
        return DomicilioSerializer

    @classmethod
    def get_definition(cls):
        return CFDI_DOMICILIO_DEFINITION or {}

    @classmethod
    def super_add(cls, data=None , tag = 'DOMICILIOFISCAL'):
        instance = None
        if data is not None and data.strip():
            soup = BeautifulSoup(data, 'xml')
            domicilio = soup.find(tag)
            if domicilio is not None:
                attributes = cls.decode(data=domicilio)
                instance = cls.objects.create()
                if instance:
                    instance.push_attributes(attributes=attributes)
        return instance

    @classmethod
    def add(cls, data=None):
        return cls.super_add(data=data)

class DomicilioFiscal(Domicilio):
    pass

    @classmethod
    def add(cls, data=None):
        return cls.super_add(data=data , tag='DOMICILIOFISCAL')

class Expedido(Domicilio):
    pass

    @classmethod
    def add(cls, data=None):
        return cls.super_add(data=data , tag='EXPEDIDOEN')

class PersonaFiscal(Base):
    ###String##################################################################
    rfc = models.TextField(default=None, null=True, blank=True)
    nombre = models.TextField(default=None, null=True, blank=True)

    @classmethod
    def get_serializer(cls):
        return None

    @property
    def rest_data(self):
        serialiser = self.__class__.get_serializer()
        if serialiser is not None:
            serialized = serialiser(self)
            return serialized.data or None
        return None

    @classmethod
    def get_definition(cls):
        return CFDI_PERSONA_FISICAL_DEFINITION or {}

    @classmethod
    def super_add(cls, data=None , tag = None):
        instance = None
        if data is not None and data.strip() and tag is not None and tag.strip():
            soup = BeautifulSoup(data, 'xml')
            emisor = soup.find(tag)
            if emisor is not None:
                attributes = cls.decode(data=emisor)
                rfc = attributes.get('rfc') or None
                if rfc is not None and rfc.strip():
                    instance = cls.objects.create(rfc=rfc)
                    if instance is not None:
                        instance.push_attributes(attributes=attributes)
                if instance is not None:
                    domicilio = Domicilio.add(data=data)
                    if domicilio is not None:
                        instance.domicilio_relation = domicilio
                        instance.save()
        return instance


class Receptor(PersonaFiscal):
    ###ForeignKey##################################################################
    domicilio_relation = models.ForeignKey('Domicilio', blank=True, null=True, related_name='cfdi_domicilio')

    @classmethod
    def get_serializer(cls):
        from serializers import ReceptorSerializer
        return ReceptorSerializer

    @property
    def domicilio(self):
        domicilio = None
        if self.domicilio_relation is not None:
            domicilio = self.domicilio_relation.rest_data
        return domicilio

    @classmethod
    def add(cls, data=None):
        instance = cls.super_add(data=data, tag='RECEPTOR')
        if instance is not None:
            domicilio = Domicilio.add(data=data)
            if domicilio is not None:
                instance.domicilio_relation = domicilio
                instance.save()
        return instance


class Emisor(PersonaFiscal):
    ###ForeignKey##################################################################
    expedido_en_relation = models.ForeignKey('Expedido', blank=True, null=True, related_name='cfdi_expedido')
    ###ManyToMany##################################################################
    regimen_fiscal_relations = models.ManyToManyField('RegimenFiscal')
    ###ForeignKey##################################################################
    domicilio_fiscal_relation = models.ForeignKey('DomicilioFiscal', blank=True, null=True, related_name='cfdi_domicilio_fiscal')

    @classmethod
    def get_serializer(cls):
        from serializers import EmisorSerializer
        return EmisorSerializer

    @property
    def domicilio_fiscal(self):
        domicilio_fiscal = None
        if self.domicilio_fiscal_relation is not None:
            domicilio_fiscal = self.domicilio_fiscal_relation.rest_data
        return domicilio_fiscal

    @property
    def regimen_fiscal(self):
        regimen_fiscal = None
        if self.regimen_fiscal_relations is not None:
            regimen_fiscal = self.regimen_fiscal_relations.rest_data
        return regimen_fiscal

    @property
    def expedido_en(self):
        expedido_en = None
        if self.expedido_en_relation is not None:
            expedido_en = self.expedido_en_relation.rest_data
        return expedido_en

    @classmethod
    def add(cls, data=None):
        instance = cls.super_add(data=data , tag = 'EMISOR')
        if instance is not None:
            expedido_en = Expedido.add(data=data)
            if expedido_en is not None:
                instance.expedido_en_relation = expedido_en
                instance.save()
            domicilio_fiscal = DomicilioFiscal.add(data=data)
            if domicilio_fiscal is not None:
                instance.domicilio_fiscal_relation = domicilio_fiscal
                instance.save()
            regimen_fiscal = RegimenFiscal.add(data=data)
            if regimen_fiscal is not None:
                instance.regimen_fiscal_relations.add(regimen_fiscal)
                instance.save()
        return instance

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
    cantidad = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    valor_unitario = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    importe = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    ###ForeignKey##################################################################
    predial_relation = models.ForeignKey('ConceptoPredial' , blank=True, null=True, related_name='concepto')
    ###ManyToMany##################################################################
    informacion_aduanera_relations = models.ManyToManyField('InformacionAduanera')
    partes_relations = models.ManyToManyField('Parte')
    complementos_relations = models.ManyToManyField('Concepto')

    @classmethod
    def get_serializer(cls):
        from serializers import ConceptoSerializer
        return ConceptoSerializer

    @classmethod
    def get_definition(cls):
        return CFDI_CONCEPTO_DEFINITION or {}

    @classmethod
    def add(cls, data=None):
        instances = []
        if data is not None and data.strip():
            soup = BeautifulSoup(data, 'xml')
            conceptos = soup.findAll('CONCEPTO')
            print "conceptos: %s" % conceptos
            for concepto in conceptos:
                attributes = cls.decode(data=concepto)
                print "attributes: %s" % attributes
                instance = cls.objects.create()
                if instance is not None:
                    instance.push_attributes(attributes=attributes)
                    instances.append(instance)
        return instances

class ImpuestosAplicaciones(models.Model):
    ###Decimal##################################################################
    impuesto = models.TextField(default=None, null=True, blank=True)
    importe = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)

    @classmethod
    def get_definition(cls):
        return {}

    @classmethod
    def get_attributes(cls):
        attributes = []
        definition = cls.get_definition()
        if definition is not None and definition.__class__ is dict:
            if 'attributes' in definition.keys():
                attributes = definition.get('attributes') or []
        return attributes

    @classmethod
    def get_required_attributes(cls):
        attributes = []
        for attr in cls.get_attributes():
            if 'required' in attr.keys() and attr.get('required') is True:
                attributes.append(attr)
        return attributes

    @classmethod
    def get_fields_keys(cls):
        return [
            {
                'key': attr.get('key'),
                'field': attr.get('name'),
            } for attr in cls.get_attributes() if
            'name' in attr.keys() and attr.get('name') is not None and 'key' in attr.keys() and attr.get('key') is not None
            ]

    @classmethod
    def get_fields(cls):
        fields = [attr.get('name') for attr in cls.get_attributes() if
                  'name' in attr.keys() and attr.get('name') is not None]
        return fields

    @classmethod
    def get_required_fields(cls):
        fields = [attr.get('name') for attr in cls.get_required_attributes() if
                  'name' in attr.keys() and attr.get('name') is not None]
        return fields

    @classmethod
    def get_keys(cls):
        fields = [attr.get('key') for attr in cls.get_attributes() if 'key' in attr.keys() and attr.get('key') is not None]
        return fields

    @classmethod
    def get_required_keys(cls):
        fields = [attr.get('key') for attr in cls.get_required_attributes() if
                  'key' in attr.keys() and attr.get('key') is not None]
        return fields

    @classmethod
    def is_required_field(cls, item):
        if cls.has_field(item) and item in cls.get_required_fields():
            return True
        return False

    @classmethod
    def has_field(cls, key=None):
        if key is not None and key in cls.fields():
            return True
        return False

    @classmethod
    def fields(cls):
        fields = cls._meta.fields
        return fields

    @classmethod
    def decode(cls, data=None):
        d = {}
        if data is not None:
            for attr in cls.get_fields_keys():
                key = attr.get('key') or None
                field = attr.get('field') or None
                if key is not None and key.strip() and field is not None and field.strip():
                    value = None
                    if data.has_attr(key):
                        value = data.get(key) or None
                    d.update({
                        field: value
                    })
        return d

    @classmethod
    def get_serializer(cls):
        return None

    @classmethod
    def filtering(cls, data=None , filtering={}):

        return data

    @classmethod
    def rest_list(cls, **kwargs):
        rest_list = []
        serialiser = cls.get_serializer()
        if serialiser is not None:
            if 'filtering' in kwargs.keys():
                filtering = kwargs.get('filtering') or {}
            else:
                filtering = {}
            if 'data' in kwargs.keys():
                data = kwargs.get('data') or None
            if data is None:
                data = cls.objects.all()
            data = cls.filtering(data = data , filtering=filtering)
            serialized = serialiser(data, many=True)
            rest_list = serialized.data or None
        return rest_list

    @property
    def rest_data(self):
        serialiser = self.__class__.get_serializer()
        if serialiser is not None:
            serialized = serialiser(self)
            return serialized.data or None
        return None

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

    def push_attributes(self, attributes = {}):
        if attributes is not None and attributes.__class__ is dict:
            for key in attributes.keys():
                value = attributes.get(key) or None
                setattr(self, key, value)
                self.save()

class Retenidos(ImpuestosAplicaciones):
    pass

    @classmethod
    def get_serializer(cls):
        from serializers import RetenidosSerializer
        return RetenidosSerializer

    @classmethod
    def get_definition(cls):
        return CFDI_RETENIDO_DEFINITION or {}

    @classmethod
    def add(cls, data=None):
        instances = []
        if data is not None and data.strip():
            soup = BeautifulSoup(data, 'xml')
            retenidos = soup.find('RETENIDOS')
            print "retenidos: %s" % retenidos
            if retenidos is not None:
                for retenido in retenidos.find_all('RETENIDO'):
                    instance = cls.objects.create()
                    if instance is not None:
                        attributes = cls.decode(data=retenido)
                        instance.push_attributes(attributes=attributes)
                        instances.append(instance)
        return instances

class Trasladado(ImpuestosAplicaciones):
    ###Decimal##################################################################
    tasa = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)

    @classmethod
    def get_serializer(cls):
        from serializers import TrasladadoSerializer
        return TrasladadoSerializer

    @classmethod
    def get_definition(cls):
        return CFDI_TRASLADADO_DEFINITION or {}

    @classmethod
    def add(cls, data=None):
        instances = []
        if data is not None and data.strip():
            soup = BeautifulSoup(data, 'xml')
            traslados = soup.find('TRASLADOS')
            print "traslados: %s" % traslados
            if traslados is not None:
                for traslado in traslados.find_all('TRASLADO'):
                    instance = cls.objects.create()
                    if instance is not None:
                        attributes = cls.decode(data=traslado)
                        instance.push_attributes(attributes=attributes)
                        instances.append(instance)
        return instances

class Impuesto(Base):
    ###Decimal##################################################################
    total_impuestos_retenidos = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    total_impuestos_trasladados = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    ###ManyToMany##################################################################
    retenidos_relations = models.ManyToManyField('Retenidos', related_name='impuesto_retenidos')
    trasladados_relations = models.ManyToManyField('Trasladado', related_name='impuesto_transladados')

    @classmethod
    def get_serializer(cls):
        from serializers import ImpuestoSerializer
        return ImpuestoSerializer

    @property
    def retenidos(self):
        retenidos = None
        if self.retenidos_relations is not None:
            retenidos = Retenidos.rest_list(data=self.retenidos_relations.all())
        return retenidos

    @property
    def trasladados(self):
        trasladados = None
        if self.trasladados_relations is not None:
            trasladados = Trasladado.rest_list(data=self.trasladados_relations.all())
        return trasladados

    @classmethod
    def get_definition(cls):
        return CFDI_IMPUESTO_DEFINITION or {}

    @classmethod
    def add(cls, data=None):
        instance = None
        if data is not None and data.strip():
            instance = cls.objects.create()
            if instance is not None:
                soup = BeautifulSoup(data, 'xml')
                impuestos = soup.find('IMPUESTOS')
                print "impuestos: %s" % impuestos
                if impuestos is not None:
                    attributes = cls.decode(data=impuestos)
                    instance.push_attributes(attributes=attributes)
                    trasladados = Trasladado.add(data = data)
                    for trasladado in trasladados:
                        instance.trasladados_relations.add(trasladado)
                    retenidos = Retenidos.add(data=data)
                    for retenido in retenidos:
                        instance.retenidos_relations.add(retenido)
                    instance.figure_retenidos
                    instance.figure_trasladados
        return instance

    def _figure_retenidos(self):
        retenidos = 0.00
        for trasladado in self.trasladados_relations.all():
            importe = trasladado.importe
            if importe is None:
                try:
                    importe = float(importe)
                except:
                    importe = 0.00
            retenidos = float(retenidos) +  float(importe)
        self.total_impuestos_trasladados = retenidos
        self.save()
    figure_retenidos = property(_figure_retenidos)


    def _figure_trasladados(self):
        trasladados = 0.00
        for retenido in self.retenidos_relations.all():
            importe = retenido.importe
            if importe is None:
                try:
                    importe = float(importe)
                except:
                    importe = 0.00
            trasladados = float(trasladados) + float(importe)
        self.total_impuestos_retenidos = trasladados
        self.save()
    figure_trasladados = property(_figure_trasladados)

class Complemento(models.Model):
    ###String##################################################################
    lead = models.TextField(default=None, null=True, blank=True)
    key = models.TextField(default=None, null=True, blank=True)
    value = models.TextField(default=None, null=True, blank=True)

class TimbreFiscalDigital(Base):
    sello_cfd = models.TextField(default=None, null=True, blank=True)
    cfd_uuid = models.TextField(default=None, null=True, blank=True)
    tfd = models.TextField(default=None, null=True, blank=True)
    sello_sat = models.TextField(default=None, null=True, blank=True)
    version = models.TextField(default=None, null=True, blank=True)
    schema_location = models.TextField(default=None, null=True, blank=True)
    xsi = models.TextField(default=None, null=True, blank=True)
    no_certificado_sat = models.TextField(default=None, null=True, blank=True)
    ###DateTime##################################################################
    fecha_timbrado = models.DateTimeField(default=None, null=True, blank=True)

    @property
    def folio_fiscal(self):
        return self.cfd_uuid or None

    @classmethod
    def get_definition(cls):
        return CFDI_TIMBRE_FISCAL_DIGITAL_DEFINITION or {}

    @classmethod
    def add(cls, data=None):
        instance = None
        if data is not None and data.strip():
            soup = BeautifulSoup(data, 'xml')
            complemento = soup.find('COMPLEMENTO')
            if complemento is not None:
                timbre_fiscal_digital = complemento.find('TIMBREFISCALDIGITAL')
                if timbre_fiscal_digital is not None:
                    attributes = cls.decode(data=timbre_fiscal_digital)
                    cfd_uuid = attributes.get('cfd_uuid') or None
                    fecha_timbrado = attributes.get('fecha_timbrado') or None
                    try:
                        fecha_timbrado = datetime.strptime(fecha_timbrado, '%Y-%m-%dT%H:%M:%S')
                    except:
                        fecha_timbrado = None
                    if cfd_uuid is not None and cfd_uuid.strip() and fecha_timbrado is not None:
                        instance, created = cls.objects.get_or_create(cfd_uuid = cfd_uuid , fecha_timbrado = fecha_timbrado)
                        if instance is not None and created is True:
                            instance.push_attributes(attributes = attributes)
        return instance

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
    subtotal = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    descuento = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    total= models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    monto_folio_fiscal_orig = models.DecimalField(default=None, null=True, blank=True, max_digits=8, decimal_places=2)
    ###ForeignKey##################################################################
    emisor_relation = models.ForeignKey('Emisor' , blank=True, null=True, related_name='cfdi_emitidas')
    receptor_relation = models.ForeignKey('Receptor' , blank=True, null=True, related_name='cfdi_recibidas')
    complemento_relation = models.ForeignKey('Complemento', blank=True, null=True, related_name='cfdi_complemento')
    timbre_fiscal_digital_relation = models.ForeignKey('TimbreFiscalDigital', blank=True, null=True, related_name='cfdi_timbre_fiscal')
#    complemento_relation = models.ForeignKey('Complemento' , blank=False, null=False, related_name='cfdi_complemento')
#    addenda_relation = models.ForeignKey('Addenda' , blank=False, null=False, related_name='cfdi_addenda')
    ###ManyToMany##################################################################
    conceptos_relations = models.ManyToManyField('Concepto')
    impuestos_relations = models.ManyToManyField('Impuesto')
#    complementos_relations = models.ManyToManyField('Complemento')
    addenda_relations = models.ManyToManyField('Addenda')

    class Meta:
        ordering = ['fecha']

    @classmethod
    def get_serializer(cls):
        from serializers import CFDISerializer
        return CFDISerializer

    @classmethod
    def get_definition(cls):
        return CFDI_COMPROBANTE_DEFINITION or {}

    @classmethod
    def add(cls, data=None):
        instance = None
        if data is not None and data.strip():
            soup = BeautifulSoup(data, 'xml')
            comprobante = soup.find('COMPROBANTE')
            if comprobante is not None:
                attributes = cls.decode(data=comprobante)
            timbre_fiscal_digital = TimbreFiscalDigital.add(data = data)
            emisor = Emisor.add(data=data)
            receptor = Receptor.add(data=data)
            if timbre_fiscal_digital is not None and emisor is not None and receptor is not None:
                instance , created = cls.objects.get_or_create(timbre_fiscal_digital_relation = timbre_fiscal_digital , emisor_relation = emisor , receptor_relation = receptor)
                if instance is not None and created is True:
                    instance.push_attributes(attributes=attributes)
                    conceptos = Concepto.add(data = data)
                    for concepto in conceptos:
                        instance.conceptos_relations.add(concepto)
                    impuesto = Impuesto.add(data=data)
                    instance.impuestos_relations.add(impuesto)
        return instance

    @property
    def impuestos(self):
        impuestos = None
        if self.impuestos_relations is not None:
            impuestos = Impuesto.rest_list(data=self.impuestos_relations.all())
        return impuestos

    @property
    def conceptos(self):
        conceptos = None
        if self.conceptos_relations is not None:
            conceptos = Concepto.rest_list(data=self.conceptos_relations.all())
        return conceptos

    @property
    def fecha_json(self):
        fecha = None
        if self.fecha is not None:
            fecha = self.fecha.isoformat()
        return fecha

    @property
    def emisor(self):
        json = None
        if self.emisor_relation is not None:
            json = self.emisor_relation.rest_data
        return json

    @property
    def receptor(self):
        json = None
        if self.receptor_relation is not None:
            json = self.receptor_relation.rest_data
        return json

    @property
    def folio_fiscal(self):
        folio_fiscal = ""
        if self.timbre_fiscal_digital_relation is not None:
            folio_fiscal = self.timbre_fiscal_digital_relation.folio_fiscal or ""
        return folio_fiscal

    @property
    def sello_cfd(self):
        sello_cfd = ""
        if self.timbre_fiscal_digital_relation is not None:
            sello_cfd = self.timbre_fiscal_digital_relation.sello_cfd or ""
        return sello_cfd

    @property
    def tfd(self):
        sello_cfd = ""
        if self.timbre_fiscal_digital_relation is not None:
            sello_cfd = self.timbre_fiscal_digital_relation.sello_cfd or ""
        return sello_cfd

    @property
    def sello_sat(self):
        sello_sat = ""
        if self.timbre_fiscal_digital_relation is not None:
            sello_sat = self.timbre_fiscal_digital_relation.sello_sat or ""
        return sello_sat

    @property
    def xsi(self):
        xsi = ""
        if self.timbre_fiscal_digital_relation is not None:
            sello_sat = self.timbre_fiscal_digital_relation.xsi or ""
        return xsi

    @property
    def fecha_timbrado(self):
        fecha_timbrado = ""
        if self.timbre_fiscal_digital_relation is not None:
            fecha_timbrado = self.timbre_fiscal_digital_relation.fecha_timbrado or ""
            fecha_timbrado = fecha_timbrado.isoformat()
        return fecha_timbrado

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

    @classmethod
    def do_process(cls):
        while cls.objects.filter(processed = False).filter(data__isnull = True).filter(cfdi__isnull = True).exists():
            instance = cls.objects.filter(processed = False).filter(data__isnull = True).filter(cfdi__isnull = True).first()
            if instance is not None:
                if instance.xml_file is not None:
                    try:
                        instance.xml_file.open()
                        data = instance.xml_file.read()
                        instance.xml_file.close()
                    except:
                        data = None
                    if data is not None:
                        data = data.upper()
                        instance.data = data
                        instance.save()
                        instance.fix_encode
                        instance.parse

    @classmethod
    def cfdi_list(cls):
        data_list = CFDI.objects.all()
        return data_list

    @property
    def process(self):
        if self.xml_file is not None:
            try:
                self.xml_file.open()
                data = self.xml_file.read()
                self.xml_file.close()
            except:
                data = None
            if data is not None:
                data = data.upper()
                self.data = data
                self.save()
                self.fix_encode
                self.parse

    @property
    def fix_encode(self):
        try:
            data = self.data
            data = data.encode('utf-8')
            data = data.decode('utf-8-sig')
            self.data = data
            self.save()
        except:
            pass

    @property
    def status(self):
        return True

    @property
    def file_name(self):
        name = None
        if self.xml_file is not None:
            name = self.xml_file.name
        return name


    @property
    def parse(self):
        if self.cfdi is None and self.data is not None and self.data.strip():
            instance = CFDI.add(self.data)
            if instance is not None:
                self.cfdi = instance
                self.processed = True
                self.save()