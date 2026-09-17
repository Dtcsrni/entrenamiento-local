# Contratos compartidos

Los archivos de `json-schema/` son la fuente versionada de los contratos que
cruzan componentes. Un cambio incompatible debe crear una nueva versión o
incluir una migración explícita.

## Validación local

Desde la raíz del repositorio:

```powershell
python scripts/validate_contracts.py
python -m unittest discover -s tests -p "test_*.py"
```

El validador usa JSON Schema Draft 2020-12 y activa la comprobación de
formatos `uuid` y `date-time`. Los ejemplos bajo `examples/` son sintéticos y
no representan datos personales.
