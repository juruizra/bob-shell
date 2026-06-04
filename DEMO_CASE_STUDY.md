# Caso de Uso: Sistema de Login con Malas Prácticas

## Objetivo del Demo

Este repositorio demuestra cómo IBM Bob Shell automatiza la detección y corrección de problemas de código en un pipeline CI/CD usando GitHub Actions y skills personalizadas.

## Escenario

Una aplicación de login bancario con **múltiples problemas de seguridad, arquitectura y calidad de código** que serán detectados y corregidos automáticamente por Bob.

## Estructura del Proyecto

```
demo-app/
├── main/                          # Rama principal (código BUENO)
│   ├── auth/
│   │   ├── login.py              # Login seguro con buenas prácticas
│   │   ├── user_manager.py       # Gestión de usuarios correcta
│   │   └── session.py            # Manejo de sesiones seguro
│   ├── database/
│   │   └── db_manager.py         # Acceso a BD con prepared statements
│   └── utils/
│       └── validators.py         # Validación de entrada robusta
│
└── dev/                           # Rama de desarrollo (código MALO)
    ├── auth/
    │   ├── login.py              # ❌ SQL Injection vulnerable
    │   ├── user_manager.py       # ❌ Viola SOLID principles
    │   └── session.py            # ❌ Hardcoded credentials
    ├── database/
    │   └── db_manager.py         # ❌ String concatenation en queries
    └── utils/
        └── validators.py         # ❌ Sin validación de entrada
```

## Problemas Intencionados en Rama `dev`

### 1. Vulnerabilidades de Seguridad
- **SQL Injection**: Queries construidos con concatenación de strings
- **Hardcoded Credentials**: Contraseñas en código fuente
- **Sin Validación de Entrada**: Acepta cualquier input del usuario
- **Logging de Datos Sensibles**: Passwords en logs
- **Sesiones Inseguras**: Sin timeout, tokens predecibles

### 2. Violaciones de SOLID
- **Single Responsibility**: Clases que hacen demasiado
- **Open/Closed**: Código difícil de extender
- **Liskov Substitution**: Herencia incorrecta
- **Interface Segregation**: Interfaces gordas
- **Dependency Inversion**: Dependencias concretas en lugar de abstracciones

### 3. Problemas de Arquitectura
- **God Class**: Clase con 500+ líneas
- **Tight Coupling**: Dependencias directas entre módulos
- **No Separation of Concerns**: Lógica de negocio mezclada con UI
- **Código Duplicado**: Mismo código en múltiples lugares

### 4. Problemas de Calidad
- **Funciones Largas**: Métodos de 100+ líneas
- **Magic Numbers**: Números sin explicación
- **Sin Documentación**: Código sin comentarios
- **Nombres Confusos**: Variables como `x`, `data`, `temp`
- **Sin Tests**: Cero cobertura de tests

## Workflows que se Activarán

### 1. Review PR with Skills
**Trigger**: Cuando se crea PR de `dev` → `main` con label `review-with-bob`

**Bob detectará:**
- 15+ vulnerabilidades de seguridad
- 20+ violaciones de SOLID
- 10+ problemas de arquitectura
- 30+ problemas de calidad

**Resultado**: Comentario detallado en el PR con todos los hallazgos

### 2. Fix PR Reviews with Bob
**Trigger**: Cuando reviewer comenta en el PR

**Ejemplo de comentario:**
```
"Esta función tiene SQL injection, por favor usa prepared statements"
```

**Bob automáticamente:**
1. Lee el comentario
2. Modifica el código para usar prepared statements
3. Hace commit al PR
4. Responde al comentario explicando el fix

### 3. Fix Issues with Bob
**Trigger**: Cuando se crea issue con label `fix-with-bob`

**Ejemplo de issue:**
```
Title: "Login permite SQL injection"
Description: "El método login() en auth/login.py concatena strings 
para construir queries SQL. Esto permite ataques de SQL injection."
```

**Bob automáticamente:**
1. Lee el issue
2. Analiza el código mencionado
3. Crea branch `fix-issue-123`
4. Corrige el problema
5. Crea PR hacia `main`
6. Comenta en el issue con link al PR

### 4. Test PR with Bob
**Trigger**: PR con label `test-with-bob`

**Bob automáticamente:**
1. Genera tests unitarios para el código nuevo
2. Genera tests de integración
3. Ejecuta los tests
4. Reporta cobertura
5. Comenta resultados en el PR

### 5. Label PRs/Issues
**Trigger**: Nuevo PR o Issue

**Bob automáticamente:**
1. Analiza el contenido
2. Aplica labels relevantes:
   - `security` si hay vulnerabilidades
   - `bug` si es un fix
   - `enhancement` si es nueva funcionalidad
   - `documentation` si actualiza docs

## Flujo de Demostración

### Paso 1: Setup Inicial
```bash
# Clonar repositorio
git clone <repo-url>
cd <repo-name>

# Verificar estructura
ls -la .bob/skills/
ls -la .github/workflows/
```

### Paso 2: Configurar Secrets
```bash
# En GitHub: Settings → Secrets → Actions
# Agregar:
# - BOBSHELL_API_KEY
# - SKILLBERRY_BOT_TOKEN (opcional)
```

### Paso 3: Crear Labels
```bash
gh label create "review-with-bob" --color "0E8A16" --description "Trigger Bob code review"
gh label create "fix-with-bob" --color "D93F0B" --description "Trigger Bob to fix issues"
gh label create "test-with-bob" --color "1D76DB" --description "Trigger Bob to generate tests"
```

### Paso 4: Demo de Review Automático
```bash
# Crear PR desde dev a main
gh pr create --base main --head dev \
  --title "Add login functionality" \
  --body "Implements user authentication system"

# Agregar label para activar Bob
gh pr edit <PR_NUMBER> --add-label "review-with-bob"

# Ver workflow ejecutándose
gh run list --workflow=review-pr-with-skills.yml

# Ver comentarios de Bob en el PR
gh pr view <PR_NUMBER>
```

### Paso 5: Demo de Fix Automático
```bash
# Comentar en el PR
gh pr comment <PR_NUMBER> --body "@skillberry-bot Esta función tiene SQL injection, usa prepared statements"

# Bob automáticamente corregirá el código
# Ver el commit de Bob
gh pr view <PR_NUMBER> --comments
```

### Paso 6: Demo de Fix de Issues
```bash
# Crear issue
gh issue create \
  --title "Login permite SQL injection" \
  --body "El método login() concatena strings en queries SQL" \
  --label "fix-with-bob"

# Bob creará un PR automáticamente
gh pr list
```

## Métricas Esperadas

### Antes de Bob (Manual)
- Tiempo de review: 2-4 horas
- Issues encontrados: 10-15 (depende del reviewer)
- Tiempo de fix: 4-8 horas
- Ciclo completo: 1-2 días

### Después de Bob (Automatizado)
- Tiempo de review: 5-10 minutos
- Issues encontrados: 50+ (consistente)
- Tiempo de fix: 10-20 minutos
- Ciclo completo: 30-60 minutos

### Mejora
- **Velocidad**: 20-40x más rápido
- **Cobertura**: 3-5x más issues detectados
- **Consistencia**: 100% (siempre aplica las mismas reglas)
- **Costo**: Reduce tiempo de developers en 80%

## Skills Personalizadas Aplicadas

1. **sql-injection-prevention**: Detecta y previene SQL injection
2. **solid-principles**: Verifica cumplimiento de SOLID
3. **security-vulnerabilities**: Detecta vulnerabilidades generales
4. **architecture-patterns**: Valida patrones de arquitectura
5. **code-quality**: Verifica calidad general del código

## Resultados Esperados

### PR Review Report (Ejemplo)
```markdown
## Bob Code Review Report

### Critical Issues (5)
1. SQL Injection in auth/login.py:45
2. Hardcoded password in auth/session.py:12
3. No input validation in utils/validators.py:23
4. Sensitive data in logs at auth/login.py:67
5. Insecure session token generation

### High Issues (12)
1. God class: UserManager has 500+ lines
2. Tight coupling between auth and database modules
3. No error handling in login flow
...

### Medium Issues (18)
...

### Low Issues (20)
...

### Summary
- Total Issues: 55
- Critical: 5
- High: 12
- Medium: 18
- Low: 20

### Recommendations
1. Refactor UserManager into smaller classes
2. Implement prepared statements for all queries
3. Add input validation layer
4. Remove hardcoded credentials
5. Implement proper session management
```

## Conclusión

Este caso de uso demuestra cómo Bob Shell puede:
1. **Detectar** problemas automáticamente
2. **Corregir** código basado en feedback
3. **Generar** tests automáticamente
4. **Etiquetar** PRs e issues inteligentemente
5. **Acelerar** el ciclo de desarrollo en 20-40x

Todo esto integrado en el pipeline CI/CD con GitHub Actions y skills personalizadas.