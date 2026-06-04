# Guía de Configuración del Laboratorio

Esta guía te ayudará a configurar el laboratorio paso a paso.

## 📋 Prerrequisitos

- [ ] Git instalado
- [ ] GitHub CLI (`gh`) instalado
- [ ] Cuenta de GitHub
- [ ] Licencia de IBM watsonx Code Assistant
- [ ] API Key de Bob Shell

## 🚀 Paso 1: Inicializar Repositorio Local

```bash
# Ya estás en el directorio del proyecto
cd c:/Users/CristhoferArhonAlegr/Documents/BobLab

# Inicializar git (si no está inicializado)
git init

# Verificar archivos
git status
```

## 🔧 Paso 2: Crear Repositorio en GitHub

```bash
# Opción A: Crear repositorio público (recomendado para demo)
gh repo create bob-cicd-automation-lab --public --source=. --remote=origin

# Opción B: Crear repositorio privado
gh repo create bob-cicd-automation-lab --private --source=. --remote=origin
```

## 🔑 Paso 3: Configurar Secrets

### 3.1 Obtener Bob Shell API Key

1. Ir a https://bob.ibm.com
2. Login con credenciales de IBM
3. Navegar a API Keys
4. Crear nueva API key con scope "Inference"
5. Copiar la API key

### 3.2 Agregar Secrets en GitHub

```bash
# Agregar BOBSHELL_API_KEY
gh secret set BOBSHELL_API_KEY

# Cuando te pida el valor, pega tu API key y presiona Enter

# Verificar que se agregó
gh secret list
```

**Nota**: `GITHUB_TOKEN` se proporciona automáticamente, no necesitas agregarlo.

## 🏷️ Paso 4: Crear Labels

```bash
# Crear labels necesarios para los workflows
gh label create "review-with-bob" --color "0E8A16" --description "Trigger Bob code review"
gh label create "fix-with-bob" --color "D93F0B" --description "Trigger Bob to fix issues"
gh label create "test-with-bob" --color "1D76DB" --description "Trigger Bob to generate tests"

# Labels adicionales útiles
gh label create "security" --color "D73A4A" --description "Security vulnerability"
gh label create "architecture" --color "0075CA" --description "Architecture issue"
gh label create "code-quality" --color "FEF2C0" --description "Code quality improvement"
gh label create "refactoring" --color "FBCA04" --description "Code refactoring needed"

# Verificar labels creados
gh label list
```

## 📝 Paso 5: Commit Inicial (Código Bueno - Main Branch)

```bash
# Asegurarte de estar en main
git checkout -b main

# Agregar archivos del código bueno
git add .gitignore
git add README.md
git add DEMO_CASE_STUDY.md
git add DEMO_ISSUES.md
git add REQUIREMENTS.md
git add WORKFLOWS_EXPLANATION.md
git add SETUP_GUIDE.md

# Agregar workflows
git add .github/

# Agregar skills
git add .bob/

# Agregar código bueno (demo-app)
git add demo-app/

# Commit inicial
git commit -m "Initial commit: Bob CI/CD Automation Lab

- Add GitHub Actions workflows for Bob Shell integration
- Add custom skills for code review
- Add demo application with best practices
- Add comprehensive documentation
"

# Push a GitHub
git push -u origin main
```

## 🔀 Paso 6: Crear Branch Dev con Código Malo

```bash
# Crear branch dev desde main
git checkout -b dev

# Agregar código malo
git add demo-app-bad/

# Commit con código malo
git commit -m "Add demo code with intentional bad practices

This code contains:
- 15+ security vulnerabilities
- 20+ SOLID violations
- 10+ architecture issues
- 30+ code quality problems

For demonstration purposes only.
"

# Push branch dev
git push -u origin dev
```

## 🎯 Paso 7: Crear PR de Demo

```bash
# Crear PR desde dev a main
gh pr create \
  --base main \
  --head dev \
  --title "Add authentication system with multiple issues" \
  --body "$(cat <<'EOF'
## Description
This PR adds a login authentication system for the banking application.

## Changes
- Add LoginManager class
- Implement user authentication
- Add session management
- Add user registration

## Testing
- Manual testing completed
- Ready for review

**Note**: This PR intentionally contains multiple issues for demonstration purposes.
EOF
)"

# Obtener número del PR
PR_NUMBER=$(gh pr list --head dev --json number --jq '.[0].number')
echo "PR Number: $PR_NUMBER"

# Agregar label para activar Bob review
gh pr edit $PR_NUMBER --add-label "review-with-bob"

# Ver el PR
gh pr view $PR_NUMBER --web
```

## 🐛 Paso 8: Crear Issues de Demo

```bash
# Ejecutar script para crear todos los issues
bash <<'EOF'
# Issue 1: SQL Injection
gh issue create \
  --title "Login permite SQL injection en autenticación" \
  --body "El método login() construye queries SQL con concatenación de strings. Severidad: Critical" \
  --label "security,critical,fix-with-bob"

# Issue 2: Hardcoded Credentials
gh issue create \
  --title "Credenciales hardcodeadas en código fuente" \
  --body "ADMIN_PASSWORD y SECRET_KEY están hardcodeados en demo-app-bad/auth/login_bad.py. Severidad: Critical" \
  --label "security,critical,fix-with-bob"

# Issue 3: SRP Violation
gh issue create \
  --title "Clase LoginManager viola Single Responsibility Principle" \
  --body "LoginManager hace demasiadas cosas: DB, auth, sessions, logging. Necesita refactoring. Severidad: High" \
  --label "architecture,refactoring,fix-with-bob"

# Issue 4: Password Logging
gh issue create \
  --title "Sistema logea passwords en texto plano" \
  --body "Passwords se loggean en texto plano en múltiples lugares. Violación de seguridad. Severidad: High" \
  --label "security,compliance,fix-with-bob"

# Issue 5: Long Functions
gh issue create \
  --title "Método register_user tiene más de 100 líneas" \
  --body "Función demasiado larga, difícil de mantener y testear. Severidad: Medium" \
  --label "code-quality,refactoring,fix-with-bob"

echo "✅ 5 issues críticos creados. Ver más en DEMO_ISSUES.md"
EOF
```

## ✅ Paso 9: Verificar Configuración

```bash
# Verificar workflows
gh workflow list

# Verificar secrets
gh secret list

# Verificar labels
gh label list

# Verificar PR
gh pr list

# Verificar issues
gh issue list --label "fix-with-bob"
```

## 🎬 Paso 10: Ver Bob en Acción

### Opción A: Review Automático del PR

```bash
# El PR ya tiene el label "review-with-bob"
# Ver workflow ejecutándose
gh run list --workflow="review-pr-with-skills.yml"

# Ver logs del workflow
gh run view --log

# Ver comentarios de Bob en el PR
gh pr view $PR_NUMBER
```

### Opción B: Fix Automático de Issue

```bash
# Los issues ya tienen label "fix-with-bob"
# Ver workflows ejecutándose
gh run list --workflow="fix-issues-with-bob.yml"

# Ver PRs creados por Bob
gh pr list --author "@me"
```

### Opción C: Fix de Comentario de Review

```bash
# Comentar en el PR
gh pr comment $PR_NUMBER --body "@skillberry-bot Esta función tiene SQL injection, por favor usa prepared statements"

# Ver workflow ejecutándose
gh run list --workflow="fix-pr-reviews-with-bob.yml"

# Ver commit de Bob
gh pr view $PR_NUMBER
```

## 📊 Paso 11: Monitorear Resultados

```bash
# Ver todos los workflows ejecutándose
gh run list

# Ver detalles de un workflow específico
gh run view <RUN_ID>

# Ver logs de un workflow
gh run view <RUN_ID> --log

# Ver PRs creados por Bob
gh pr list

# Ver issues resueltos
gh issue list --state closed
```

## 🔍 Troubleshooting

### Problema: Workflow no se ejecuta

```bash
# Verificar que el secret existe
gh secret list

# Verificar que el label existe
gh label list | grep "review-with-bob"

# Ver logs del workflow
gh run list --workflow="review-pr-with-skills.yml"
gh run view <RUN_ID> --log
```

### Problema: Bob no comenta en el PR

```bash
# Verificar permisos del workflow
# En GitHub: Settings → Actions → General → Workflow permissions
# Debe estar en "Read and write permissions"

# Verificar que BOBSHELL_API_KEY es válido
# Probar manualmente con Bob CLI
```

### Problema: Issues no se resuelven automáticamente

```bash
# Verificar que el issue tiene el label correcto
gh issue view <ISSUE_NUMBER>

# Verificar que el workflow se ejecutó
gh run list --workflow="fix-issues-with-bob.yml"

# Ver logs para errores
gh run view <RUN_ID> --log
```

## 📚 Recursos Adicionales

- [README.md](README.md) - Documentación principal
- [DEMO_CASE_STUDY.md](DEMO_CASE_STUDY.md) - Caso de uso detallado
- [DEMO_ISSUES.md](DEMO_ISSUES.md) - Issues de ejemplo
- [REQUIREMENTS.md](REQUIREMENTS.md) - Requisitos y costos
- [WORKFLOWS_EXPLANATION.md](WORKFLOWS_EXPLANATION.md) - Explicación de workflows

## 🎓 Próximos Pasos

1. ✅ Configuración completada
2. 🔄 Observar Bob en acción
3. 📝 Documentar resultados
4. 🎯 Crear presentación del demo
5. 🚀 Compartir con el equipo

## 💡 Tips para la Demo

1. **Preparar Screenshots**: Captura pantallas de:
   - PR con comentarios de Bob
   - Issues resueltos automáticamente
   - Workflows ejecutándose
   - Commits de Bob

2. **Preparar Métricas**:
   - Tiempo de review: Manual vs Bob
   - Número de issues detectados
   - Tiempo de resolución

3. **Preparar Narrativa**:
   - Problema inicial
   - Solución con Bob
   - Resultados obtenidos
   - ROI estimado

---

**¡Configuración Completa!** 🎉

Tu laboratorio está listo para demostrar cómo Bob Shell automatiza el ciclo de vida de desarrollo.