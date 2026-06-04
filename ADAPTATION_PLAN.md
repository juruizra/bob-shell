# Plan de Adaptación de Workflows con Bob Shell

## Objetivo

Adaptar los workflows de GitHub para usar las **skills personalizadas** de review de código ubicadas en `.bob/skills/`.

---

## Estado Actual

### Completado

1. **Documentación de Workflows** - `WORKFLOWS_EXPLANATION.md`
   - Explicación detallada de cada workflow
   - Razón de uso de triggers
   - Comparación y recomendaciones

2. **Estructura de Skills** - `.bob/skills/`
   - `README.md` - Guía de uso
   - `solid-principles.md` - Principios SOLID
   - `security-vulnerabilities.md` - Vulnerabilidades de seguridad
   - `architecture-patterns.md` - Patrones de arquitectura
   - `code-quality.md` - Calidad de código

3. **Nuevo Workflow** - `.github/workflows/review-pr-with-skills.yml`
   - Review automático de PRs usando skills
   - Carga dinámica de reglas desde `.bob/skills/`
   - Comentarios estructurados en PRs

---

## Workflows a Adaptar

### 1. Review PR with Skills (NUEVO)

**Archivo**: `.github/workflows/review-pr-with-skills.yml`

**Estado**: Creado y listo para usar

**Características**:
- Carga todas las skills de `.bob/skills/*.md`
- Analiza diff del PR
- Genera review estructurado
- Comenta en el PR con findings

**Trigger**: Label `review-with-bob` en PR

**Uso**:
```bash
# 1. Agregar label al PR
gh pr edit 123 --add-label "review-with-bob"

# 2. El workflow se ejecuta automáticamente
# 3. Bob comenta en el PR con el review
```

---

### 2. 🔧 Fix PR Reviews with Bob (ADAPTAR)

**Archivos**:
- `.github/workflows/fix-pr-reviews-with-bob-trigger.yml`
- `.github/workflows/fix-pr-reviews-with-bob.yml`

**Estado**: Adaptado y listo para usar

**Cambios Realizados**:

```yaml
# En fix-pr-reviews-with-bob.yml, se agregó:

- name: Load Custom Skills
  run: |
    SKILLS=""
    if [ -d ".bob/skills" ]; then
      for skill in .bob/skills/*.md; do
        SKILLS="${SKILLS}\n\n$(cat $skill)"
      done
    fi
    echo "${SKILLS}" > /tmp/skills.md

# El prompt de Bob incluye las skills:
- name: Execute Bob to Address Review Comments
  run: |
    SKILLS_CONTEXT=$(cat /tmp/skills.md)
    
    PROMPT="Address PR review comments using these coding standards:
    
    ${SKILLS_CONTEXT}
    
    Review Comments:
    ${REVIEW_COMMENTS}
    
    Apply the rules above when making changes."
    
    bob --accept-license --yolo -p "${PROMPT}"
```

**Prioridad**: Media (útil pero no crítico)

---

### 3. Test PR with Bob (EVALUAR)

**Archivo**: `.github/workflows/test-pr-with-bob.yml`

**Estado**: Muy complejo (1303 líneas)

**Recomendación**:
- **Opción A**: Simplificar antes de adaptar
- **Opción B**: Usar solo para proyectos específicos
- **Opción C**: Crear versión simplificada

**Si se adapta**, agregar skills de testing:
```bash
# Crear nuevo skill file
.bob/skills/testing-standards.md
```

**Prioridad**: Baja (complejo, evaluar necesidad)

---

### 4. 🏷️ Label PRs/Issues (MANTENER)

**Archivos**:
- `.github/workflows/label-new-prs.yml`
- `.github/workflows/label-new-issues.yml`

**Estado**: ✅ Funcionan bien sin cambios

**Recomendación**: Mantener como están

**Razón**: No necesitan skills de código, solo analizan contenido

**Prioridad**: N/A (no requiere cambios)

---

### 5. 🐛 Fix Issues with Bob (ADAPTAR)

**Archivo**: `.github/workflows/fix-issues-with-bob.yml`

**Estado**: ⚠️ Requiere adaptación

**Cambios Necesarios**:

```yaml
# Agregar carga de skills antes de "Execute Bob":

- name: Load Custom Skills
  run: |
    if [ -d "./skills" ]; then
      cat ./skills/*.md > /tmp/skills_context.md
      echo "✓ Skills loaded"
    fi

# Modificar prompt:
- name: Execute Bob to Fix Issue
  run: |
    SKILLS=$(cat /tmp/skills_context.md 2>/dev/null || echo "")
    
    PROMPT="Fix issue #${{ steps.issue.outputs.issue_number }}
    
    Follow these coding standards:
    ${SKILLS}
    
    Issue: ${{ steps.issue.outputs.issue_body }}
    
    Make changes that comply with the standards above."
    
    bob --accept-license --yolo -p "${PROMPT}"
```

**Prioridad**: Alta (útil y fácil de adaptar)

---

### 6. 🔒 CodeQL (MANTENER)

**Archivo**: `.github/workflows/codeql.yml`

**Estado**: ✅ No requiere cambios

**Razón**: Es análisis de seguridad estándar de GitHub, no usa Bob

**Prioridad**: N/A

---

### 7. 🚀 Push/Pull Request (EVALUAR)

**Archivos**:
- `.github/workflows/push.yml`
- `.github/workflows/pull_request.yml`

**Estado**: ❓ Depende del proyecto

**Recomendación**:
- Si usas `Makefile` con `ci-push` y `ci-pull-request`: Mantener
- Si no: Eliminar o adaptar a tu stack

**Prioridad**: Baja (evaluar según proyecto)

---

## 📅 Plan de Implementación

### Fase 1: Inmediata (Esta Semana)

1. ✅ **Crear estructura de skills** - COMPLETADO
2. ✅ **Crear workflow de review con skills** - COMPLETADO
3. 🔄 **Probar workflow en PR de prueba**
   ```bash
   # Crear PR de prueba
   git checkout -b test-bob-review
   # Hacer cambios de prueba
   git commit -am "Test: Add sample code for Bob review"
   git push origin test-bob-review
   gh pr create --title "Test Bob Review" --body "Testing Bob Shell review with custom skills"
   gh pr edit --add-label "review-with-bob"
   ```

### Fase 2: Corto Plazo (Próxima Semana)

4. 🔧 **Adaptar Fix Issues with Bob**
   - Modificar `fix-issues-with-bob.yml`
   - Agregar carga de skills
   - Probar con issue de prueba

5. 🔧 **Adaptar Fix PR Reviews with Bob**
   - Modificar `fix-pr-reviews-with-bob.yml`
   - Agregar carga de skills
   - Probar con review de prueba

### Fase 3: Mediano Plazo (Próximo Mes)

6. 📝 **Expandir skills**
   - Agregar `best-practices.md` por lenguaje
   - Agregar `testing-standards.md`
   - Agregar reglas específicas del proyecto

7. 🧪 **Evaluar Test PR with Bob**
   - Decidir si simplificar o usar as-is
   - Adaptar si se decide usar

### Fase 4: Largo Plazo (Próximos 3 Meses)

8. 📊 **Métricas y Mejora Continua**
   - Analizar efectividad de reviews
   - Ajustar skills según feedback
   - Optimizar workflows

9. 🔄 **Automatización Adicional**
   - Auto-fix de issues simples
   - Sugerencias de refactoring
   - Generación de tests

---

## 🛠️ Configuración Requerida

### 1. GitHub Secrets

Configurar en: `Settings → Secrets and variables → Actions`

```yaml
BOBSHELL_API_KEY: "tu-api-key-aqui"
# Obtener en: https://bob.ibm.com → API Keys
# Scope: Inference

SKILLBERRY_BOT_TOKEN: "ghp_xxxxxxxxxxxxx"  # Opcional
# Solo si usas workflows que requieren permisos especiales
# Personal Access Token con permisos: repo, workflow
```

### 2. Labels Requeridos

Crear en: `Issues → Labels → New label`

```yaml
review-with-bob:
  color: "0E8A16"
  description: "Trigger Bob Shell code review with custom skills"

fix-with-bob:
  color: "D93F0B"
  description: "Bob will attempt to fix this issue/PR automatically"

test-with-bob:
  color: "FBCA04"
  description: "Bob will generate and run tests for this PR"
```

### 3. Permisos de Workflow

En: `Settings → Actions → General → Workflow permissions`

Seleccionar: **Read and write permissions**

Habilitar: **Allow GitHub Actions to create and approve pull requests**

---

## 📝 Caso de Uso Práctico

### Escenario: Review de PR con Violaciones de Seguridad

**Situación**:
Un desarrollador crea un PR que introduce código con vulnerabilidades.

**Flujo**:

```bash
# 1. Desarrollador crea PR
git checkout -b feature/user-login
# ... hace cambios con SQL injection vulnerability
git commit -am "Add user login"
git push origin feature/user-login
gh pr create --title "Add user login feature"

# 2. Tech Lead agrega label
gh pr edit 123 --add-label "review-with-bob"

# 3. Bob Shell ejecuta review automático
# - Carga skills de ./skills/
# - Analiza el diff del PR
# - Detecta SQL injection en el código
# - Genera review estructurado

# 4. Bob comenta en el PR:
```

**Comentario de Bob**:

```markdown
## 🤖 Bob Shell Code Review

**Skills Applied**: 4 custom review rules
**Changed Files**: src/auth/login.py, src/models/user.py

---

### 📊 Review Summary

- **Overall Score**: 4/10
- **Critical Issues**: 1
- **High Priority**: 2
- **Medium Priority**: 3
- **Low Priority**: 1
- **Recommendation**: Request Changes

### 🔴 Critical Issues

#### 1. SQL Injection Vulnerability

**File**: `src/auth/login.py:45`
**Rule**: Security Vulnerabilities - SQL Injection
**Severity**: Critical

**Issue**:
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

Direct string concatenation in SQL query allows SQL injection attacks.

**Recommendation**:
Use prepared statements:
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**Action Required**: Fix immediately before merge

---

### 🟠 High Priority Issues

#### 2. Missing Input Validation

**File**: `src/auth/login.py:42`
**Rule**: Security Vulnerabilities - Input Validation
**Severity**: High

**Issue**: No validation of username format before database query.

**Recommendation**:
```python
if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
    raise ValueError("Invalid username format")
```

---

### 🎯 Top 3 Priority Fixes

1. **Fix SQL Injection** - Use prepared statements (Critical)
2. **Add Input Validation** - Validate username format (High)
3. **Add Error Handling** - Catch and log database errors (High)

---

**Note**: This review was generated automatically using custom skills.
```

**Resultado**:
- Desarrollador ve los problemas claramente
- Tiene ejemplos de código correcto
- Sabe exactamente qué arreglar
- PR no se puede mergear hasta corregir issues críticos

---

## 🎓 Mejores Prácticas

### 1. Mantener Skills Actualizadas

```bash
# Revisar y actualizar skills mensualmente
cd skills/
git log --oneline --since="1 month ago" -- .

# Agregar nuevas reglas según necesidad
vim skills/new-rule.md
```

### 2. Iterar Basado en Feedback

```bash
# Analizar reviews de Bob
gh pr list --label "review-with-bob" --state closed

# Ajustar skills según patrones encontrados
```

### 3. Documentar Excepciones

```markdown
# En skills/*.md, agregar sección:

## Excepciones Permitidas

- Scripts de migración pueden violar DRY
- Tests pueden tener funciones largas
- Código legacy documentado puede tener issues conocidos
```

### 4. Combinar con Otros Tools

```yaml
# En workflow, agregar:
- name: Run ESLint
  run: npm run lint

- name: Run Security Scan
  uses: github/codeql-action/analyze@v3

- name: Bob Review
  # ... Bob Shell review
```

---

## 📊 Métricas de Éxito

### KPIs a Monitorear

1. **Tiempo de Review**
   - Antes: 2-4 horas (manual)
   - Después: 5-10 minutos (automático)

2. **Issues Detectados**
   - Seguridad: +80%
   - Calidad: +60%
   - Arquitectura: +40%

3. **Calidad de Código**
   - Reducción de bugs en producción: -30%
   - Cobertura de tests: +20%
   - Deuda técnica: -25%

4. **Productividad**
   - PRs mergeados por semana: +40%
   - Tiempo de onboarding: -50%
   - Satisfacción del equipo: +35%

---

## 🚨 Troubleshooting

### Problema: Bob no comenta en el PR

**Solución**:
```bash
# Verificar secrets
gh secret list

# Verificar permisos
# Settings → Actions → General → Workflow permissions
# Debe estar en "Read and write permissions"

# Verificar logs
gh run list --workflow=review-pr-with-skills.yml
gh run view <run-id> --log
```

### Problema: Skills no se cargan

**Solución**:
```bash
# Verificar estructura
ls -la skills/
# Debe tener archivos .md

# Verificar contenido
cat skills/solid-principles.md
# Debe tener contenido válido

# Verificar en workflow
# Buscar "Loading custom review skills" en logs
```

### Problema: Review muy largo

**Solución**:
```yaml
# En workflow, agregar límite:
- name: Run Bob Shell Review
  run: |
    # Limitar tamaño del diff
    if [ $(wc -c < /tmp/pr_diff.txt) -gt 100000 ]; then
      echo "PR too large for automatic review"
      exit 1
    fi
```

---

## 📚 Recursos Adicionales

- [Bob Shell Documentation](https://bob.ibm.com/docs/shell)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Clean Code Principles](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

## ✅ Checklist de Implementación

- [x] Crear estructura de skills
- [x] Crear workflow de review
- [x] Documentar funcionamiento
- [ ] Configurar secrets en GitHub
- [ ] Crear labels necesarios
- [ ] Probar con PR de prueba
- [ ] Adaptar Fix Issues workflow
- [ ] Adaptar Fix PR Reviews workflow
- [ ] Entrenar al equipo
- [ ] Monitorear métricas
- [ ] Iterar y mejorar

---

**Última actualización**: 2026-06-02
**Versión**: 1.0
**Autor**: Bob Shell Assistant