# 📚 Explicación Completa de GitHub Workflows con Bob Shell

## 🎯 Resumen Ejecutivo

Estos workflows automatizan tareas de desarrollo usando **IBM Bob Shell** (IA para código):

1. **Fix PR Reviews** - Bob corrige automáticamente comentarios de revisión en PRs
2. **Test PR** - Bob genera y ejecuta tests automáticamente
3. **Label PRs** - Bob etiqueta PRs automáticamente según contenido
4. **Fix Issues** - Bob crea PRs para resolver issues etiquetados
5. **CodeQL** - Análisis de seguridad estándar de GitHub
6. **Push/PR** - Workflows básicos de CI/CD

---

## 🔄 ¿Por qué se usan TRIGGERS?

### Problema de Seguridad en GitHub

GitHub tiene una **limitación de seguridad crítica**:

```
❌ Los eventos de PRs desde forks NO tienen acceso a secrets del repositorio
✅ Los eventos workflow_run SÍ tienen acceso a secrets
```

### Solución: Patrón Trigger + Worker

```
┌─────────────────────────────────────────────────────────┐
│  TRIGGER WORKFLOW (sin secrets)                         │
│  - Se ejecuta en el contexto del fork                   │
│  - Captura información del PR/Review                    │
│  - Guarda datos en artifact                             │
│  - Completa exitosamente                                │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ workflow_run event
                 ▼
┌─────────────────────────────────────────────────────────┐
│  WORKER WORKFLOW (con secrets)                          │
│  - Se ejecuta en el contexto del repo base              │
│  - Descarga artifact del trigger                        │
│  - Tiene acceso a BOBSHELL_API_KEY                      │
│  - Ejecuta Bob Shell y hace cambios                     │
└─────────────────────────────────────────────────────────┘
```

**Ejemplo Práctico:**

```yaml
# TRIGGER: fix-pr-reviews-with-bob-trigger.yml
on:
  pull_request_review:  # ❌ No tiene acceso a secrets desde forks
    types: [submitted]

# Guarda contexto en artifact
- name: Upload PR review context
  uses: actions/upload-artifact@v7
  with:
    name: pr-review-context
    path: pr-review-context.json

---

# WORKER: fix-pr-reviews-with-bob.yml  
on:
  workflow_run:  # ✅ SÍ tiene acceso a secrets
    workflows: ["Fix PR Reviews with Bob - Trigger"]
    types: [completed]

# Descarga contexto y usa secrets
env:
  BOBSHELL_API_KEY: ${{ secrets.BOBSHELL_API_KEY }}  # ✅ Funciona aquí
```

---

## 📋 Workflows Detallados

### 1. 🔧 Fix PR Reviews with Bob

**¿Qué hace?**
Cuando un reviewer deja comentarios en un PR, Bob **automáticamente corrige el código** según esos comentarios.

**Flujo:**

```
1. Reviewer deja comentarios en PR
2. PR debe tener label "fix-with-bob"
3. Comentario debe mencionar "@skillberry-bot"
   ↓
4. TRIGGER workflow captura contexto
5. WORKER workflow descarga contexto
6. Bob Shell lee todos los comentarios
7. Bob modifica el código para abordar cada comentario
8. Commits automáticos al branch del PR
9. Bob responde a cada comentario explicando cambios
```

**Ejemplo de Uso:**

```markdown
# Reviewer comenta en PR:
"Este método es muy largo, deberías dividirlo en funciones más pequeñas"

# Bob automáticamente:
1. Refactoriza el método
2. Crea funciones auxiliares
3. Hace commit: "Address review comments from @reviewer"
4. Responde: "✅ He dividido el método en 3 funciones más pequeñas..."
```

**Archivos:**
- `fix-pr-reviews-with-bob-trigger.yml` - Captura evento de review
- `fix-pr-reviews-with-bob.yml` - Ejecuta Bob y hace cambios

---

### 2. 🧪 Test PR with Bob

**¿Qué hace?**
Bob **genera tests automáticamente** para el código del PR y los ejecuta.

**Flujo:**

```
1. Se abre/actualiza un PR
2. PR debe tener label "test-with-bob"
   ↓
3. Bob analiza el código del PR
4. Bob genera tests (unit, integration, e2e)
5. Bob ejecuta los tests
6. Bob genera reportes de cobertura
7. Bob comenta en el PR con resultados
```

**Características:**
- Genera tests con Playwright para frontend
- Genera tests unitarios para backend
- Ejecuta tests y captura screenshots/videos
- Reporta cobertura de código
- Commits tests al PR si pasan

**Archivo:**
- `test-pr-with-bob.yml` - Workflow completo (1303 líneas)

---

### 3. 🏷️ Label New PRs

**¿Qué hace?**
Bob **etiqueta automáticamente** PRs nuevos según su contenido.

**Flujo:**

```
1. Se abre un nuevo PR
   ↓
2. Bob analiza:
   - Título del PR
   - Descripción
   - Archivos modificados
   - Labels disponibles en el repo
   ↓
3. Bob selecciona labels relevantes
4. Bob aplica los labels al PR
5. Bob comenta explicando su elección
```

**Ejemplo:**

```
PR: "Add user authentication with JWT"
Archivos: src/auth/jwt.ts, src/middleware/auth.ts

Bob aplica:
- 🔐 security
- ✨ enhancement
- 🔧 backend
```

**¿Usa Bob?** ✅ SÍ - Bob analiza el PR y selecciona labels inteligentemente

**Archivos:**
- `label-new-prs-trigger.yml` - Captura evento de PR nuevo
- `label-new-prs.yml` - Bob analiza y etiqueta

---

### 4. 🐛 Fix Issues with Bob

**¿Qué hace?**
Bob **crea un PR automáticamente** para resolver un issue.

**Flujo:**

```
1. Agregas label "fix-with-bob" a un issue
   ↓
2. Bob lee la descripción del issue
3. Bob analiza el código relacionado
4. Bob hace cambios para resolver el issue
5. Bob crea un nuevo branch: fix-issue-{número}
6. Bob hace commit de los cambios
7. Bob crea un PR hacia main
8. Bob comenta en el issue con link al PR
```

**Ejemplo:**

```
Issue #42: "El botón de login no funciona en mobile"

Bob:
1. Analiza el componente de login
2. Identifica problema de CSS responsive
3. Corrige los estilos
4. Crea PR: "Fix: Issue #42 - El botón de login no funciona en mobile"
5. Comenta: "🤖 He creado un PR con la solución propuesta"
```

**¿Usa Bob?** ✅ SÍ - Bob analiza el issue y genera código

**Archivo:**
- `fix-issues-with-bob.yml` - Workflow completo

---

### 5. 🔍 Label New Issues

**¿Qué hace?**
Similar a Label PRs pero para issues.

**¿Usa Bob?** ✅ SÍ - Bob analiza issues y aplica labels

**Archivo:**
- `label-new-issues.yml` - Bob etiqueta issues

---

### 6. 🔒 CodeQL

**¿Qué hace?**
Análisis de seguridad estándar de GitHub (NO usa Bob).

**¿Es necesario?** ✅ SÍ - Detecta vulnerabilidades de seguridad

**Análisis:**
- SQL Injection
- XSS
- Hardcoded credentials
- Insecure dependencies

**Archivo:**
- `codeql.yml` - Análisis de seguridad

---

### 7. 🚀 Push / Pull Request

**¿Qué hacen?**
Workflows básicos de CI/CD (NO usan Bob).

**¿Son necesarios?** 
- ❓ **Depende de tu proyecto**
- Si tienes un `Makefile` con comandos `ci-push` y `ci-pull-request`, son útiles
- Si no, puedes eliminarlos o adaptarlos

**Archivos:**
- `push.yml` - Se ejecuta en push a main
- `pull_request.yml` - Se ejecuta en PRs

---

## 🎯 Workflows Recomendados para Tu Proyecto

### ✅ MANTENER (Usan Bob):

1. **fix-pr-reviews-with-bob** - Muy útil para automatizar correcciones
2. **label-new-prs** - Automatiza organización
3. **fix-issues-with-bob** - Acelera resolución de issues

### ⚠️ EVALUAR:

4. **test-pr-with-bob** - Útil pero complejo (1303 líneas)
5. **codeql** - Recomendado para seguridad

### ❌ ELIMINAR (si no aplican):

6. **push.yml** - Solo si no usas Make
7. **pull_request.yml** - Solo si no usas Make

---

## 🔑 Secrets Requeridos

Debes configurar en GitHub Settings → Secrets:

```yaml
BOBSHELL_API_KEY: "tu-api-key-de-bob"
# Obtener en: bob.ibm.com → API Keys → Scope: Inference

SKILLBERRY_BOT_TOKEN: "ghp_xxxxxxxxxxxxx"
# Personal Access Token con permisos:
# - repo (full control)
# - workflow
```

---

## 📊 Comparación de Workflows

| Workflow | Usa Bob | Trigger | Necesario | Complejidad |
|----------|---------|---------|-----------|-------------|
| Fix PR Reviews | ✅ | ✅ | ⭐⭐⭐ | Media |
| Test PR | ✅ | ✅ | ⭐⭐ | Alta |
| Label PRs | ✅ | ✅ | ⭐⭐ | Baja |
| Fix Issues | ✅ | ❌ | ⭐⭐⭐ | Media |
| Label Issues | ✅ | ❌ | ⭐ | Baja |
| CodeQL | ❌ | ❌ | ⭐⭐⭐ | Baja |
| Push/PR | ❌ | ❌ | ❓ | Baja |

---

## 🎓 Conceptos Clave

### "Corrige automáticamente comentarios de review"

Significa que cuando un reviewer dice:
- "Este código tiene un bug"
- "Falta validación de entrada"
- "Deberías usar async/await"

Bob **modifica el código automáticamente** para implementar esos cambios.

### Modo `--yolo`

```bash
bob --yolo -p "Fix this code"
```

- `--yolo` = Permite a Bob **escribir archivos**
- Sin `--yolo` = Bob solo lee y sugiere
- Necesario en CI/CD para hacer cambios automáticos

### Workflow Artifacts

```yaml
- uses: actions/upload-artifact@v7
  with:
    name: pr-review-context
    path: context.json
```

Artifacts = Archivos temporales compartidos entre workflows
- Duración: 1-90 días
- Uso: Pasar datos del trigger al worker

---

## 🚀 Próximos Pasos

1. ✅ Entender cómo funcionan los workflows
2. 🔄 Crear carpeta `./skills` con reglas personalizadas
3. 🔧 Adaptar workflows para usar tus skills
4. 📝 Documentar caso de uso específico
5. 🧪 Probar en un PR de prueba