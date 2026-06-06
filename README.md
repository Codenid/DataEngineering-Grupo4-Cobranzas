# Proyecto de Ingeniería de Datos - Optimización de Cobranzas

---

# Descripción del Proyecto

Este proyecto tiene como objetivo construir la base tecnológica y de datos para analizar la efectividad de las estrategias de cobranza aplicadas a distintos segmentos de clientes morosos dentro de una empresa del sector telecomunicaciones.

La solución implementa un pipeline de datos que permite la ingesta diaria, almacenamiento histórico y trazabilidad de información relacionada con:

* Cartera de clientes morosos
* Gestiones de cobranza realizadas
* Recuperos obtenidos

La información es almacenada en una capa RAW (Bronze) dentro de un Data Lake, constituyendo la base para futuras capacidades analíticas y Data Products orientados a maximizar la recuperación de deuda minimizando el costo operativo.

---

# Problema de Negocio

Las empresas de telecomunicaciones ejecutan múltiples estrategias de cobranza para recuperar deuda vencida.

Sin embargo, no siempre existe visibilidad sobre:

* Qué estrategia genera mejores resultados.
* Qué agencia obtiene mayor efectividad.
* Qué segmentos presentan mejor recuperación.
* Cuál es el costo asociado a cada gestión.

La pregunta central del negocio es:

> ¿Cómo maximizar la recuperación de deuda minimizando el costo de gestión?

---

# Contexto Funcional

## Segmentos de Cobranza

| Segmento       | Rango          |
| -------------- | -------------- |
| Super Temprana | 7 días         |
| Temprana       | 15 días        |
| Masiva         | 0 - 90 días    |
| Tardía         | Más de 91 días |

## Estrategias

* Llamadas
* BOT
* IA

## Agencias

* RECSA
* Cobranding
* COM (Call Center Interno)

---

# Objetivo de la Primera Entrega

Construir un pipeline de datos hasta la capa RAW que permita:

* Ingestar información diariamente.
* Mantener histórico de datos.
* Garantizar trazabilidad.
* Registrar auditoría de ejecuciones.
* Preparar la base para futuras capas Silver y Gold.

---

# Alcance

## Incluye

* Ingesta diaria de archivos.
* Validación de archivos fuente.
* Orquestación mediante Apache Airflow.
* Carga histórica en Data Lake.
* Registro de auditoría.
* Manejo de errores y trazabilidad.

## No Incluye

* Transformaciones de negocio.
* KPIs.
* Dashboards.
* Modelos analíticos.
* Machine Learning.
* Data Products finales.

---

# Arquitectura

```text
┌─────────────┐
│ Fuentes CSV │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Airflow   │
│ Orquestador │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Data Lake   │
│ RAW/Bronze  │
└─────────────┘
```

Flujo:

Local → Airflow → Data Lake RAW

---

# Datasets

| Dataset               | Tipo          |
| --------------------- | ------------- |
| cartera_diaria.csv    | Transaccional |
| gestiones_diarias.csv | Transaccional |
| recuperos_diarios.csv | Transaccional |

---

# Pipeline Implementado

## DAG

**cobranzas_raw_ingestion**

### Frecuencia

* Diaria

### Actividades

1. Validación de archivos fuente.
2. Lectura de datasets.
3. Registro de auditoría.
4. Carga hacia capa RAW.
5. Validación de ejecución.

---

# Controles Implementados

El pipeline contempla:

* Archivo inexistente.
* Archivo vacío.
* Error de conexión al Data Lake.
* Error de auditoría.
* Errores inesperados de ejecución.

---

# Estructura del Proyecto

```text
.
├── dags/
├── plugins/
├── scripts/
├── config/
├── logs/
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

---

# Tecnologías Utilizadas

* Python
* Apache Airflow
* Docker
* Docker Compose
* Azure Data Lake Storage Gen2
* Git
* GitHub

---

# Estrategia Git

Se adoptó GitFlow para garantizar un desarrollo colaborativo y controlado.

## Ramas

### main

Versión estable del proyecto.

### develop

Rama de integración continua.

### feature/*

Ramas de desarrollo de funcionalidades.

Ejemplo:

```text
feature/dag-cobranzas-raw-ingestion
```

---

# Flujo de Desarrollo

```text
feature/*
    │
    ▼
develop
    │
    ▼
main
```

Proceso:

1. Desarrollo en feature.
2. Push a feature.
3. Pull Request hacia develop.
4. Validación.
5. Integración.
6. Release hacia main.

---

# Resultados Obtenidos

## Validación del DAG

* Ejecución satisfactoria.
* Orquestación completa del pipeline.
* Registro de auditoría generado.

## Outputs Generados

Archivos almacenados en la capa RAW:

* cartera
* gestiones
* recuperos

Organizados por fecha de procesamiento para soportar trazabilidad e históricos.

---

# Aprendizajes

Durante el desarrollo del proyecto se identificó la importancia de:

* Diseñar arquitecturas escalables.
* Mantener trazabilidad de los datos.
* Implementar procesos idempotentes.
* Separar responsabilidades entre orquestación y almacenamiento.
* Construir capas RAW que faciliten la evolución hacia Silver y Gold.

Asimismo, se comprendió el funcionamiento operativo de los procesos de cobranza y la relevancia de medir la efectividad por estrategia, agencia y segmento.

---

# Próximos Pasos

## Silver

Consolidación y limpieza de información.

Posibles tablas:

* fact_cartera
* fact_gestiones
* fact_recuperos

## Gold

Generación de métricas y KPIs.

Posibles productos:

* Efectividad por estrategia.
* Efectividad por agencia.
* Recuperación por segmento.
* Costo por recupero.
* Ranking de estrategias.
* Predicción de recupero.

---

# Data Product Objetivo

El Data Product final permitirá responder preguntas como:

* ¿Qué estrategia recupera más deuda?
* ¿Qué agencia tiene mejor desempeño?
* ¿Qué segmentos presentan mayor probabilidad de pago?
* ¿Cómo reducir costos operativos manteniendo la efectividad?

Con ello se busca optimizar la gestión de cobranzas mediante decisiones basadas en datos.

---

# Repositorio

https://github.com/Codenid/DataEngineering-Grupo4-Cobranzas