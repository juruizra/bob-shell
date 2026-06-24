---
name: trailing-spaces-check
description: Revisión de espacios vacíos en finales de línea o saltos de línea al final del archivos, trailing spaces.
---

# Trailing Spaces Check Skill

## Objetivo
Detectar y reportar espacios en blanco innecesarios al final de las líneas de código y saltos de línea excesivos al final de los archivos.

## Reglas Estrictas

### 1. Espacios al Final de Línea (Trailing Spaces)
- **DEBE** identificar cualquier espacio, tabulación o carácter de espacio en blanco al final de una línea de código
- **DEBE** reportar la ubicación exacta (archivo, número de línea) de cada ocurrencia
- **DEBE** contar el número total de espacios trailing encontrados por línea
- **NO DEBE** ignorar ningún tipo de archivo de código fuente (incluyendo .py, .js, .ts, .java, .cpp, .go, .rb, .php, .html, .css, .md, .json, .yaml, .xml, etc.)
- **DEBE** verificar archivos de configuración (.gitignore, .env, .config, etc.)

### 2. Líneas Vacías al Final del Archivo (Trailing Newlines)
- **DEBE** detectar si hay más de una línea vacía al final de cualquier archivo
- **DEBE** reportar archivos que no terminan con exactamente un salto de línea
- **DEBE** reportar archivos que terminan con múltiples líneas vacías consecutivas
- **DEBE** verificar que el archivo termine con un único carácter de nueva línea (\n)

### 3. Severidad de Issues
- Espacios trailing en código: **medium**
- Múltiples líneas vacías al final: **low**
- Archivos sin salto de línea final: **low**
- Espacios trailing en archivos de configuración críticos (.env, .gitignore): **high**

### 4. Categorización
- **category**: "style"
- **type**: "inconsistent-formatting"

## Proceso de Análisis

### Paso 1: Identificación de Archivos
1. Listar todos los archivos en el directorio del proyecto
2. Filtrar archivos binarios y directorios excluidos (.git, node_modules, __pycache__, .venv, dist, build)
3. Priorizar archivos de código fuente y configuración

### Paso 2: Análisis Línea por Línea
Para cada archivo:
1. Leer el contenido completo del archivo
2. Analizar cada línea individualmente
3. Detectar espacios en blanco al final usando regex: `[ \t]+$`
4. Registrar número de línea y cantidad de espacios

### Paso 3: Análisis de Final de Archivo
Para cada archivo:
1. Verificar los últimos caracteres del archivo
2. Contar líneas vacías consecutivas al final
3. Verificar presencia de salto de línea final
4. Determinar si cumple con el estándar (exactamente un \n al final)

### Paso 4: Generación de Reportes
1. Crear un issue por cada archivo con problemas
2. Agrupar múltiples ocurrencias del mismo archivo en un solo issue
3. Incluir sugerencias de corrección específicas
4. Proporcionar comando para corrección automática si es posible

## Formato de Reporte

### Para Trailing Spaces
```
title: "Trailing spaces detected in [filename]"
message: "Found [N] line(s) with trailing whitespace:
- Line [X]: [N] trailing space(s)
- Line [Y]: [N] trailing space(s)

Trailing spaces can cause unnecessary git diffs and inconsistencies in version control."

suggestion: "Remove all trailing whitespace. In most editors:
- VS Code: Enable 'files.trimTrailingWhitespace' setting
- Vim: Use :%s/\s\+$//e
- Manual: Review and remove spaces at end of lines [X], [Y]"
```

### Para Trailing Newlines
```
title: "Incorrect file ending in [filename]"
message: "File has [N] trailing newlines (expected: 1)

Files should end with exactly one newline character for POSIX compliance and consistent git behavior."

suggestion: "Ensure file ends with exactly one newline character.
- Remove extra blank lines at end of file
- Add missing newline if file doesn't end with one"
```

## Exclusiones
- **NO** analizar archivos en: .git/, node_modules/, __pycache__/, .venv/, venv/, dist/, build/, .next/, .nuxt/
- **NO** analizar archivos binarios: .png, .jpg, .jpeg, .gif, .ico, .pdf, .zip, .tar, .gz, .exe, .dll, .so
- **NO** analizar archivos generados automáticamente (package-lock.json, yarn.lock, poetry.lock)

## Comandos de Corrección Sugeridos

### Para proyectos Python:
```bash
# Usar autopep8 o black para formateo automático
autopep8 --in-place --aggressive --aggressive [file]
black [file]
```

### Para proyectos JavaScript/TypeScript:
```bash
# Usar prettier
prettier --write [file]
```

### Comando universal (sed):
```bash
# Remover trailing spaces
sed -i 's/[[:space:]]*$//' [file]
```

## Integración con Git Hooks
Sugerir al usuario configurar un pre-commit hook:
```bash
# .git/hooks/pre-commit
#!/bin/sh
git diff --cached --name-only | while read file; do
    if [ -f "$file" ]; then
        sed -i 's/[[:space:]]*$//' "$file"
        git add "$file"
    fi
done
```

## Métricas de Calidad
- **Crítico**: > 50 líneas con trailing spaces en un archivo
- **Alto**: 20-50 líneas con trailing spaces
- **Medio**: 5-19 líneas con trailing spaces
- **Bajo**: 1-4 líneas con trailing spaces

## Notas Importantes
- Los trailing spaces son considerados "code smell" en la mayoría de guías de estilo
- Pueden causar conflictos innecesarios en merge/pull requests
- Algunos lenguajes (como Python) pueden tener problemas con trailing spaces en ciertos contextos
- La mayoría de IDEs modernos pueden configurarse para eliminar trailing spaces automáticamente al guardar