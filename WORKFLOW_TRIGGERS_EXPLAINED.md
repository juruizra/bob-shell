# 🔔 Explicación de Triggers y Ejecución de Workflows

## 📋 Resumen Ejecutivo

Los workflows de Bob se ejecutan **automáticamente** en respuesta a eventos específicos de GitHub. Aquí está cómo y cuándo se ejecuta cada uno:

---

## 🤖 1. Review PR with Skills

### Trigger
```yaml
on:
  pull_request:
    types: [opened, synchronize, labeled]
```

### ¿Cuándo se ejecuta?
- ✅ **Automático**: Cuando se agrega el label `review-with-bob` a un PR
- ✅ **Automático**: Cuando se actualiza un PR que ya tiene el label
- ✅ **Automático**: Cuando se abre un PR con el label

### ¿Cómo funciona?
```
1. Desarrollador crea PR
2. Tech Lead agrega label "review-with-bob"
   ↓
3. GitHub detecta el label → Ejecuta workflow automáticamente
4. Bob analiza el código con skills
5. Bob comenta en el PR con findings
```

### Ejemplo de Uso
```bash
# Crear PR
gh pr create --title "Add login feature"

# Agregar label (esto DISPARA el workflow automáticamente)
gh pr edit 123 --add-label "review-with-bob"

# Bob comenta automáticamente en ~5-10 minutos
```

### ¿Se ejecuta en cada comentario?
❌ **NO** - Solo se ejecuta cuando:
- Se agrega el label por primera vez
- Se hace push al PR (si ya tiene el label)

---

## 🔧 2. Fix PR Reviews with Bob

### Trigger
```yaml
on:
  pull_request_review:
    types: [submitted]
```

### ¿Cuándo se ejecuta?
- ✅ **Automático**: Cada vez que un reviewer **ENVÍA** un review con comentarios
- ✅ **Automático**: Solo si el PR tiene label `fix-with-bob`
- ✅ **Automático**: Solo si el review menciona `@skillberry-bot`

### ¿Cómo funciona?
```
1. Reviewer hace review del PR con comentarios
2. Reviewer hace clic en "Submit review"
   ↓
3. GitHub detecta review → Ejecuta workflow automáticamente
4. Bob lee TODOS los comentarios del review
5. Bob modifica el código para abordar cada comentario
6. Bob hace commit al PR
7. Bob responde a cada comentario explicando cambios
```

### Ejemplo de Uso
```bash
# 1. PR debe tener el label
gh pr edit 123 --add-label "fix-with-bob"

# 2. Reviewer hace review en GitHub UI:
# - Agrega comentarios en líneas específicas
# - Menciona @skillberry-bot en el review
# - Hace clic en "Submit review"

# 3. Bob automáticamente:
# - Lee todos los comentarios
# - Modifica el código
# - Hace commit
# - Responde a cada comentario
```

### ¿Responde a CADA comentario individual?
❌ **NO** - Solo responde cuando se **ENVÍA el review completo**

✅ **SÍ** - Responde a TODOS los comentarios del review en una sola ejecución

### Flujo Visual
```
Reviewer escribe comentario 1 → No pasa nada
Reviewer escribe comentario 2 → No pasa nada
Reviewer escribe comentario 3 → No pasa nada
Reviewer hace clic "Submit review" → ¡BOB SE EJECUTA!
   ↓
Bob lee comentarios 1, 2, 3
Bob hace cambios para los 3
Bob hace 1 commit
Bob responde a los 3 comentarios
```

---

## 🐛 3. Fix Issues with Bob

### Trigger
```yaml
on:
  issues:
    types: [labeled]
```

### ¿Cuándo se ejecuta?
- ✅ **Automático**: Cuando se agrega el label `fix-with-bob` a un issue
- ❌ **NO** se ejecuta al crear el issue
- ❌ **NO** se ejecuta al comentar en el issue

### ¿Cómo funciona?
```
1. Alguien crea un issue describiendo un bug
2. Tech Lead agrega label "fix-with-bob"
   ↓
3. GitHub detecta el label → Ejecuta workflow automáticamente
4. Bob lee la descripción del issue
5. Bob analiza el código relacionado
6. Bob hace cambios para resolver el issue
7. Bob crea un nuevo branch: fix-issue-{número}
8. Bob hace commit de los cambios
9. Bob crea un PR hacia main
10. Bob comenta en el issue con link al PR
```

### Ejemplo de Uso
```bash
# 1. Crear issue
gh issue create --title "Login button not working" --body "When I click login, nothing happens"

# 2. Agregar label (esto DISPARA el workflow)
gh issue edit 42 --add-label "fix-with-bob"

# 3. Bob automáticamente:
# - Crea branch: fix-issue-42
# - Hace cambios
# - Crea PR
# - Comenta en el issue
```

---

## 🏷️ 4. Label PRs/Issues

### Trigger
```yaml
on:
  pull_request:
    types: [opened]
  issues:
    types: [opened]
```

### ¿Cuándo se ejecuta?
- ✅ **Automático**: Cuando se crea un nuevo PR
- ✅ **Automático**: Cuando se crea un nuevo issue
- ❌ **NO** requiere label

### ¿Cómo funciona?
```
1. Desarrollador crea PR o issue
   ↓
2. GitHub detecta creación → Ejecuta workflow automáticamente
3. Bob analiza título, descripción, archivos
4. Bob selecciona labels relevantes
5. Bob aplica los labels automáticamente
6. Bob comenta explicando su elección
```

---

## 🔒 5. CodeQL Security Scan

### Trigger
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Semanal
```

### ¿Cuándo se ejecuta?
- ✅ **Automático**: En cada push a main
- ✅ **Automático**: En cada PR hacia main
- ✅ **Automático**: Cada domingo a medianoche
- ❌ **NO** usa Bob (es análisis de GitHub)

### ¿Bob puede interpretar resultados de CodeQL?
✅ **SÍ** - Puedes crear un workflow que:
1. Ejecuta CodeQL
2. Lee los resultados
3. Pasa resultados a Bob para análisis
4. Bob explica vulnerabilidades en lenguaje simple

### Ejemplo de Integración Bob + CodeQL
```yaml
- name: Run CodeQL
  uses: github/codeql-action/analyze@v3

- name: Get CodeQL Results
  run: |
    # Obtener resultados de CodeQL
    gh api /repos/${{ github.repository }}/code-scanning/alerts > codeql-results.json

- name: Bob Analyzes CodeQL Results
  run: |
    RESULTS=$(cat codeql-results.json)
    PROMPT="Analyze these CodeQL security findings and explain them:
    
    ${RESULTS}
    
    For each finding:
    1. Explain the vulnerability in simple terms
    2. Show the risk level
    3. Provide fix recommendations
    4. Show example of secure code"
    
    echo "${PROMPT}" | bob --accept-license > codeql-analysis.md

- name: Comment Analysis
  run: |
    gh pr comment ${{ github.event.pull_request.number }} \
      --body-file codeql-analysis.md
```

---

## 📊 Tabla Comparativa de Triggers

| Workflow | Trigger | Automático | Requiere Label | Frecuencia |
|----------|---------|------------|----------------|------------|
| **Review PR with Skills** | PR opened/updated | ✅ | ✅ `review-with-bob` | Por PR |
| **Fix PR Reviews** | Review submitted | ✅ | ✅ `fix-with-bob` | Por review |
| **Fix Issues** | Label added | ✅ | ✅ `fix-with-bob` | Por issue |
| **Label PRs** | PR opened | ✅ | ❌ | Por PR |
| **Label Issues** | Issue opened | ✅ | ❌ | Por issue |
| **CodeQL** | Push/PR/Schedule | ✅ | ❌ | Múltiple |

---

## 🎯 Casos de Uso Detallados

### Caso 1: Review Completo de PR

**Objetivo**: Obtener review automático de código

**Pasos**:
```bash
# 1. Crear PR
git checkout -b feature/new-api
git commit -am "Add new API endpoint"
git push origin feature/new-api
gh pr create --title "Add new API endpoint"

# 2. Solicitar review de Bob
gh pr edit 123 --add-label "review-with-bob"

# 3. Esperar ~5-10 minutos
# Bob comenta automáticamente con:
# - Issues de seguridad
# - Violaciones de SOLID
# - Problemas de arquitectura
# - Issues de calidad de código
```

**Resultado**: Comentario estructurado con findings

---

### Caso 2: Corrección Automática de Review

**Objetivo**: Bob corrige automáticamente comentarios de reviewer

**Pasos**:
```bash
# 1. PR debe tener label
gh pr edit 123 --add-label "fix-with-bob"

# 2. Reviewer hace review en GitHub:
# - Comenta: "Esta función es muy larga, dividirla"
# - Comenta: "Falta validación de input"
# - Comenta: "Usar prepared statements para SQL"
# - Menciona @skillberry-bot en el review
# - Hace clic "Submit review"

# 3. Bob automáticamente (en ~10-15 min):
# - Divide la función larga
# - Agrega validación de input
# - Cambia a prepared statements
# - Hace commit: "Address review comments from @reviewer"
# - Responde a cada comentario explicando cambios
```

**Resultado**: Código corregido + respuestas a comentarios

---

### Caso 3: Fix Automático de Issue

**Objetivo**: Bob crea PR para resolver issue

**Pasos**:
```bash
# 1. Crear issue
gh issue create \
  --title "SQL Injection in login endpoint" \
  --body "The /api/login endpoint uses string concatenation for SQL queries"

# 2. Agregar label
gh issue edit 42 --add-label "fix-with-bob"

# 3. Bob automáticamente (en ~15-20 min):
# - Analiza el código de login
# - Identifica la vulnerabilidad
# - Cambia a prepared statements
# - Crea branch: fix-issue-42
# - Hace commit con fix
# - Crea PR hacia main
# - Comenta en issue: "🤖 Created PR #123 to fix this issue"
```

**Resultado**: PR listo para review

---

## 🔄 ¿Se puede crear un Hook para comentarios individuales?

### Opción 1: Webhook Personalizado (Avanzado)

✅ **SÍ** - Puedes crear un webhook que responda a cada comentario:

```yaml
# .github/workflows/respond-to-comments.yml
name: Respond to PR Comments

on:
  issue_comment:
    types: [created]

jobs:
  respond:
    if: |
      github.event.issue.pull_request &&
      contains(github.event.comment.body, '@bob')
    runs-on: ubuntu-latest
    steps:
      - name: Respond to Comment
        run: |
          COMMENT="${{ github.event.comment.body }}"
          
          PROMPT="Respond to this PR comment:
          
          ${COMMENT}
          
          Provide a helpful response."
          
          RESPONSE=$(echo "${PROMPT}" | bob --accept-license)
          
          gh pr comment ${{ github.event.issue.number }} \
            --body "${RESPONSE}"
```

### Opción 2: Bot Interactivo (Muy Avanzado)

Crear un bot que:
1. Escucha comentarios en tiempo real
2. Responde inmediatamente
3. Puede hacer cambios de código
4. Mantiene contexto de conversación

**Requiere**:
- Servidor dedicado
- Webhook endpoint
- Base de datos para contexto
- Más complejo de mantener

### Recomendación

Para la mayoría de casos, el **workflow actual es suficiente**:
- Reviewer hace review completo
- Bob responde a todos los comentarios juntos
- Más eficiente y menos costoso

---

## 💡 Tips y Mejores Prácticas

### 1. Usar Labels Estratégicamente

```bash
# Review automático en PRs críticos
gh pr edit 123 --add-label "review-with-bob"

# Auto-fix solo en PRs de confianza
gh pr edit 123 --add-label "fix-with-bob"

# Combinar ambos
gh pr edit 123 --add-label "review-with-bob,fix-with-bob"
```

### 2. Workflow Manual (On-Demand)

Agregar trigger manual a cualquier workflow:

```yaml
on:
  workflow_dispatch:
    inputs:
      pr_number:
        description: 'PR number to review'
        required: true
```

Ejecutar manualmente:
```bash
gh workflow run review-pr-with-skills.yml -f pr_number=123
```

### 3. Notificaciones

Configurar notificaciones de Slack/Teams cuando Bob termina:

```yaml
- name: Notify Team
  if: success()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -d '{"text":"Bob completed review of PR #${{ github.event.pull_request.number }}"}'
```

---

## 🚨 Limitaciones y Consideraciones

### Límites de GitHub Actions

- **Tiempo máximo**: 6 horas por job
- **Concurrencia**: Depende del plan (20-60 jobs simultáneos)
- **Costo**: Gratis para repos públicos, minutos limitados en privados

### Límites de Bob Shell

- **Tamaño de prompt**: ~200K tokens
- **PRs muy grandes**: Pueden fallar o tomar mucho tiempo
- **Rate limits**: API de Bob tiene límites de requests

### Soluciones

```yaml
# Limitar tamaño de diff
- name: Check PR Size
  run: |
    DIFF_SIZE=$(git diff --stat | tail -1 | awk '{print $4}')
    if [ "$DIFF_SIZE" -gt 10000 ]; then
      echo "PR too large for automatic review"
      exit 1
    fi
```

---

## 📚 Resumen Final

| Pregunta | Respuesta |
|----------|-----------|
| ¿Bob responde a cada comentario? | ❌ No, solo cuando se envía el review completo |
| ¿Se ejecuta automáticamente? | ✅ Sí, con los triggers configurados |
| ¿Requiere intervención manual? | ❌ No, solo agregar labels |
| ¿Se puede ejecutar manualmente? | ✅ Sí, con workflow_dispatch |
| ¿Funciona con CodeQL? | ✅ Sí, se puede integrar |
| ¿Se puede crear hook para comentarios? | ✅ Sí, pero no recomendado |

---

**Última actualización**: 2026-06-02
**Versión**: 1.0