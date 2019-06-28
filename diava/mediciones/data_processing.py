# -*- coding: utf-8 -*-
"""
Procesamiento de datos
"""
import os
import json
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
from hashlib import blake2b
from jinja2 import Template
from django.conf import settings


#1. CONFIGURACIONES

# la carpeta donde van a estar los archivos de mediciones
carpeta_mediciones = os.path.join(settings.MEDIA_ROOT, 'mediciones')

#2. MANEJO DE ARCHIVOS Y DATOS



class ProcesamientoMedicion(object):

    def iniciar(self, nombre, serial_equipo, muestreo, *args, **kwargs):
        # datos de la medicion
        self.nombre = nombre
        self.ruta_archivo = os.path.join(carpeta_mediciones, nombre)
        ident = blake2b(self.nombre.encode(encoding='utf-8'),digest_size=10)
        self.identificador = ident.hexdigest()
        muestreos = cargar_muestreos()
        self.equipo = serial_equipo
        # datos tomados
        self.datos = []
        self.datos_originales = []
        self.timestamps = []
        self.rango = [-1,1] if self.equipo == 'unset' else equipos[self.equipo]['rango']
        self.ignorar_muestreo = False
        self.muestreo = muestreo
        self.cargar_archivo()
        # configuraciones de graficas
        self.dpi = 200
        self.nombre_grafico = '{0.equipo}_{0.identificador}'.format(self)

    def __str__(self, *args, **kwargs):
        return '[{0.equipo}] {0.nombre}'.format(self) if self.nombre else 'empty'

    def cargar_archivo(self):
        filas = self.registro_datos if self.registro_datos else self.cargar_datos_archivo()
        # calcular los tiempos y armar la matriz de mediciones
        for fila in filas:
            estampa_tiempo = datetime.strptime('_'.join(fila[:2]),'%d/%m/%Y_%H:%M:%S')
            valores = [float(v.replace(',','.')) for v in fila[2:]]
            self.datos.append([estampa_tiempo.timestamp()] + valores)
            self.datos_originales.append([estampa_tiempo] + valores)
            self.timestamps.append(estampa_tiempo)
        # transformar tiempo a escala de minutos
        timestamps_grafica = [a[0]/60 for a in self.datos]
        # hacer que el tiempo empiece en cero minutos
        self.initial = min(timestamps_grafica)
        if not self.ignorar_muestreo:
            self.recortar_a_muestreo()
            timestamps_grafica = [a[0]/60 for a in self.datos]
        # calcular los vectores para graficar
        self.x_axis = np.array([a - self.initial for a in timestamps_grafica])
        self.y_axis = np.array([a[1:] for a in self.datos])
        return self.datos

    def cargar_datos_archivo(self):
        # leer el texto bruto del archivo y partirlo en filas y columnas
        with open(self.ruta_archivo, 'r') as f:
            texto_bruto = f.read()
            filas = [
                linea.split('\t')
                for linea in texto_bruto.split('\n')
                if len(linea) > 2
                ]
        return filas

    def recortar_a_muestreo(self):
        """
        Recorta los datos entre el tiempo inicial y final configurados en
        el archivo rangos.json
        """
        menor = 0 if self.muestreo[0] == 'inicio' else int(self.muestreo[0])
        mayor = 900 if self.muestreo[1] == 'fin' else int(self.muestreo[1])
        self.datos = [
            a
            for a in self.datos
            if ((a[0]/60) -self.initial) > menor and ((a[0]/60) -self.initial) < mayor
            ]

    def calcular_maximos_minimos(self):
        """
        Calcula el valor minimo y maximo medidos
        """
        maximo = max([max(a[1:]) for a in self.datos])
        minimo = min([min(a[1:]) for a in self.datos])
        return {
            'max': maximo,
            'min': minimo
            }

    def calcular_fuera_rango(self):
        """
        Calcula las mediciones que estan fuera del rango de medicion
        """
        # obtener minimo y maximo de las configuraciones
        maximo = max(self.rango)
        minimo = min(self.rango)
        total = 0
        datos_fuera = 0
        puntos = []
        # buscar en los datos los menores al rango minimo y mayores al maximo
        for fila in self.datos:
            for registro in fila[1:]:
                if registro > maximo or registro < minimo:
                    datos_fuera += 1
                    puntos.append(registro)
                total += 1
        return {
            'total': datos_fuera,
            'porcentaje': 100 * (datos_fuera / total),
            'puntos': puntos
            }

    def calcular_promedio_desviacion(self):
        """
        Calcula el promedio y desviacion estandar total y para cada sensor
        """
        sensores_prom = []
        sensores_desv = []
        # calcula promedio por sensor
        for i in range(len(self.datos[0])-1):
            sensores_prom.append(
                np.average([a[i] for a in self.y_axis])
                )
            sensores_desv.append(
                np.std([a[i] for a in self.y_axis])
                )
        return {
            'promedio': {
                'total': np.average(self.y_axis),
                'sensores': sensores_prom
                },
            'desviacion': {
                'total': np.std(self.y_axis),
                'sensores': sensores_desv
                }
        }

    def graficar_datos(self):
        """
        Crea una grafica de las mediciones de los datos y las guarda como
        imagen .png
        """
        # crea grafica
        plt.plot(self.x_axis, self.y_axis)
        # pone titulo a grafica
        # plt.title('{0.equipo} {0.identificador}'.format(self))
        # pone etiquetas en el eje x y y
        plt.ylabel('Temperatura (C°)')
        plt.xlabel('Tiempo (Minutos)')
        # pone leyendas a las lineas
        plt.figlegend(
            ('sensor 1','sensor 2','sensor 3','sensor 4'),
            )
        # activa la grilla
        plt.grid()
        # guarda la figura
        plt.savefig(
            '{}.png'.format(
                os.path.join(carpeta_mediciones, self.nombre_grafico)
                    ),
            dpi=1.5 * self.dpi
            )
        # re-inicia la grafica para hacer un nuevo dibujo
        plt.clf()


def cargar_mediciones():
    """
    Encuentra los archivos de mediciones (los que terminan en .TXT)
    """
    archivos_mediciones = [
        Medicion(archivo)
        for archivo in os.listdir(carpeta_mediciones)
        if archivo.endswith('.TXT')
        ]
    return archivos_mediciones


def get_eq(item):
    return item['nombre']
