from rest_framework import serializers
from models import *

class CFDISerializer(serializers.ModelSerializer):
    class Meta:
        model = CFDI
        fields = ('id' , 'uuid' , 'folio_fiscal' , 'emisor' , 'receptor' , 'total' , 'subtotal' , 'fecha_json' , 'descuento' , 'lugar_expedicion' , 'folio' , 'version' , 'serie' , 'forma_de_pago' , 'condiciones_de_pago' , 'motivo_descuento' , 'tipo_cambio' , 'modena' , 'tipo_de_comprobante' , 'metodo_de_pago' , 'num_cta_pago' , 'no_certificado' , 'certificado' , 'sello' , 'sello_cfd' , 'sello_sat' , 'xsi' , 'fecha_timbrado' , 'conceptos' , 'impuestos')

class EmisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emisor
        fields = ('id' , 'uuid' , 'rfc' , 'nombre' , 'domicilio_fiscal' , 'domicilio_fiscal' , 'expedido_en')

class ReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptor
        fields = ('id' , 'uuid' , 'rfc' , 'nombre' , 'domicilio')

class DomicilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domicilio
        fields = ('id' , 'uuid' , 'calle' , 'no_exterior' , 'no_interior' , 'colonia' , 'localidad' , 'referencia' , 'municipio' , 'estado' , 'pais' , 'codigo_postal')

class ConceptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concepto
        fields = ('id', 'uuid', 'unidad', 'no_identificacion', 'descripcion' , 'cantidad' , 'valor_unitario' , 'importe')

class ImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impuesto
        fields = ('id', 'uuid', 'total_impuestos_retenidos', 'total_impuestos_trasladados' , 'retenidos' , 'trasladados')

class TrasladadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trasladado
        fields = ('id', 'impuesto', 'importe', 'tasa')

class RetenidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retenidos
        fields = ('id', 'impuesto', 'importe')