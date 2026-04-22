# FAA Neurofeedback — Contexto del Proyecto

## Descripción
Sistema de neurofeedback en tiempo real basado en EEG que calcula el **Frontal Alpha Asymmetry (FAA)** y lo muestra visualmente al usuario.

## Arquitectura

```
EEG Hardware
    └─→ OpenViBE (FAA2 (1).xml)
            └─→ LSL Export (stream name: "FAA")
                    └─→ faa_neurofeedback.py (GUI Tkinter)
```

## Archivos

| Archivo | Descripción |
|---|---|
| `FAA2 (1).xml` | Escenario activo de OpenViBE (usar este) |
| `FAA2.xml` | Versión anterior del escenario |
| `Procesamient de la señal.xml` | Escenario auxiliar |
| `faa_neurofeedback.py` | Script Python — recibe FAA vía LSL y muestra gradiente visual |
| `faa_values.csv` | CSV generado por OpenViBE con valores FAA |

## Pipeline OpenViBE (`FAA2 (1).xml`)

1. **Acquisition client** → señal EEG cruda
2. **Channel Selector 3:5** → selecciona canales frontales (F3, F4)
3. **Temporal Filter x2** → filtro de banda alpha (8–13 Hz)
4. Split en **Canal 1** (izquierdo) y **Canal 2** (derecho)
5. Cada rama: **Time based epoching** → **Signal average** → **Simple DSP** (`x*x`, potencia)
6. **Simple DSP final**: `log(B) - log(A)` = valor FAA
7. Salidas: **LSL Export** + **Signal display** + **CSV File Writer**

## Script Python (`faa_neurofeedback.py`)

- Recibe el stream LSL con `resolve_streams()` (acepta cualquier stream disponible)
- Muestra una ventana Tkinter con fondo que va de **negro** (FAA negativo) a **blanco** (FAA positivo)
- Umbral ajustable con `+`/`-` (default `±1.0`)
- Refresco cada 50 ms

### Parámetros clave
```python
FAA_RANGE = 1.0   # rango ± esperado del FAA
UPDATE_MS = 50    # refresco de pantalla
```

## Para correr el sistema

1. Abrir `FAA2 (1).xml` en **OpenViBE Designer**
2. Verificar que el box **LSL Export** esté conectado al Simple DSP final (stream name: `FAA`)
3. Dar Play ▶ en OpenViBE
4. Ejecutar: `python faa_neurofeedback.py`

## Dependencias Python
```
pylsl
tkinter (incluido en Python estándar)
```

## Notas
- El FAA positivo (derecha > izquierda) se asocia a estados de acercamiento/motivación
- El FAA negativo se asocia a estados de retirada/aversión
- La pantalla gris neutro (`#808080`) indica FAA ≈ 0
