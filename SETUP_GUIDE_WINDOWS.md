# Guía de Configuración para Windows (Sin GitHub CLI)

Esta guía te ayudará a configurar el laboratorio usando PowerShell y la interfaz web de GitHub.

## 📋 Prerrequisitos

- [x] Git instalado
- [x] PowerShell
- [ ] Cuenta de GitHub
- [ ] Licencia de IBM watsonx Code Assistant
- [ ] API Key de Bob Shell

## 🔧 Opción 1: Instalar GitHub CLI (Recomendado)

### Instalar con winget
```powershell
winget install --id GitHub.cli
```

### Instalar con Chocolatey
```powershell
choco install gh
```

### Instalar con Scoop
```powershell
scoop install gh
```

Después de instalar, cierra y abre PowerShell nuevamente, luego:
```powershell
gh auth login
```

---

## 🌐 Opción 2: Configuración Manual (Sin GitHub CLI)

### Paso 1: Crear Repositorio en GitHub

1. Ir a https://github.com/new
2. Configurar:
   - **Repository name**: `bob-cicd-automation-lab`
   - **Description**: "Automatización Inteligente de CI/CD con IBM Bob Shell"
   - **Visibility**: Public (recomendado para demo)
   - **NO** inicializar con README, .gitignore o license
3. Click en "Create repository"
4. Copiar la URL del repositorio (ej: `https://github.com/tu-usuario/bob-cicd-automation-lab.git`)

### Paso 2: Inicializar Git Local

```powershell
# Navegar al directorio del proyecto
cd C:\Users\CristhoferArhonAlegr\Documents\BobLab

# Inicializar git
git init

# Configurar usuario (si no está configurado)
git config user.name "Tu Nombre"
git config user.email "tu-email@example.com"

# Crear rama main
git checkout -b main

# Agregar remote (reemplaza con tu URL)
git remote add origin https://github.com/TU-USUARIO/bob-cicd-automation-lab.git
```

### Paso 3: Commit Inicial (Código Bueno)

```powershell
# Agregar archivos
git add .gitignore
git add README.md
git add SETUP_GUIDE.md
git add SETUP_GUIDE_WINDOWS.md
git add DEMO_CASE_STUDY.md
git add DEMO_ISSUES.md
git add REQUIREMENTS.md
git add WORKFLOWS_EXPLANATION.md
git add ADAPTATION_PLAN.md
git add WORKFLOW_TRIGGERS_EXPLAINED.md

# Agregar workflows
git add .github/

# Agregar skills
git add .bob/

# Agregar código bueno
git add demo-app/

# Ver archivos staged
git status

# Commit
git commit -m "Initial commit: Bob CI/CD Automation Lab

- Add GitHub Actions workflows for Bob Shell integration
- Add custom skills for code review (official structure)
- Add demo application with best practices
- Add comprehensive documentation
"

# Push a GitHub
git push -u origin main
```

### Paso 4: Crear Branch Dev con Código Malo

```powershell
# Crear branch dev
git checkout -b dev

# Agregar código malo
git add demo-app-bad/

# Commit
git commit -m "Add demo code with intentional bad practices

This code contains:
- 15+ security vulnerabilities (SQL injection, hardcoded credentials)
- 20+ SOLID violations (SRP, OCP, LSP, ISP, DIP)
- 10+ architecture issues (God class, tight coupling)
- 30+ code quality problems (magic numbers, long functions)

For demonstration purposes only.
"

# Push branch dev
git push -u origin dev
```

### Paso 5: Configurar Secrets en GitHub (Interfaz Web)

1. Ir a tu repositorio en GitHub
2. Click en **Settings** (arriba a la derecha)
3. En el menú izquierdo: **Secrets and variables** → **Actions**
4. Click en **New repository secret**
5. Configurar:
   - **Name**: `BOBSHELL_API_KEY`
   - **Secret**: Pegar tu API key de Bob Shell
6. Click en **Add secret**

**Cómo obtener Bob Shell API Key:**
1. Ir a https://bob.ibm.com
2. Login con credenciales de IBM
3. Navegar a **API Keys**
4. Click en **Create new API key**
5. Scope: **Inference**
6. Copiar la API key generada

### Paso 6: Crear Labels en GitHub (Interfaz Web)

1. Ir a tu repositorio en GitHub
2. Click en **Issues** (menú superior)
3. Click en **Labels** (al lado de Milestones)
4. Click en **New label** para cada uno:

**Label 1: review-with-bob**
- Name: `review-with-bob`
- Description: `Trigger Bob code review`
- Color: `#0E8A16` (verde)

**Label 2: fix-with-bob**
- Name: `fix-with-bob`
- Description: `Trigger Bob to fix issues`
- Color: `#D93F0B` (rojo)

**Label 3: test-with-bob**
- Name: `test-with-bob`
- Description: `Trigger Bob to generate tests`
- Color: `#1D76DB` (azul)

**Labels adicionales útiles:**
- `security` - Color: `#D73A4A`
- `architecture` - Color: `#0075CA`
- `code-quality` - Color: `#FEF2C0`
- `refactoring` - Color: `#FBCA04`
- `critical` - Color: `#B60205`
- `compliance` - Color: `#5319E7`

### Paso 7: Crear Pull Request (Interfaz Web)

1. Ir a tu repositorio en GitHub
2. Click en **Pull requests** (menú superior)
3. Click en **New pull request**
4. Configurar:
   - **base**: `main`
   - **compare**: `dev`
5. Click en **Create pull request**
6. Completar:
   - **Title**: `Add authentication system with multiple issues`
   - **Description**:
     ```markdown
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
     ```
7. Click en **Create pull request**
8. En el PR creado, agregar label:
   - Click en **Labels** (lado derecho)
   - Seleccionar `review-with-bob`

### Paso 8: Crear Issues (Interfaz Web)

Para cada issue en [DEMO_ISSUES.md](DEMO_ISSUES.md):

1. Ir a **Issues** → **New issue**
2. Copiar título y descripción del DEMO_ISSUES.md
3. Agregar labels correspondientes
4. Click en **Submit new issue**

**Issues críticos para crear:**

**Issue 1: SQL Injection**
- Title: `Login permite SQL injection en autenticación`
- Labels: `security`, `critical`, `fix-with-bob`

**Issue 2: Hardcoded Credentials**
- Title: `Credenciales hardcodeadas en código fuente`
- Labels: `security`, `critical`, `fix-with-bob`

**Issue 3: SRP Violation**
- Title: `Clase LoginManager viola Single Responsibility Principle`
- Labels: `architecture`, `refactoring`, `fix-with-bob`

**Issue 4: Password Logging**
- Title: `Sistema logea passwords en texto plano`
- Labels: `security`, `compliance`, `fix-with-bob`

**Issue 5: Long Functions**
- Title: `Método register_user tiene más de 100 líneas`
- Labels: `code-quality`, `refactoring`, `fix-with-bob`

### Paso 9: Verificar Workflows

1. Ir a **Actions** (menú superior)
2. Deberías ver workflows ejecutándose:
   - "Review PR with Custom Skills"
   - "Fix Issues with Bob"
3. Click en un workflow para ver detalles
4. Click en un job para ver logs

### Paso 10: Ver Bob en Acción

#### En el Pull Request:
1. Ir al PR creado
2. Esperar a que el workflow "Review PR with Custom Skills" termine
3. Ver comentarios de Bob con todos los hallazgos
4. Bob debería detectar 50+ problemas

#### En los Issues:
1. Ir a un issue con label `fix-with-bob`
2. Esperar a que el workflow "Fix Issues with Bob" termine
3. Bob creará un PR automáticamente para resolver el issue
4. Bob comentará en el issue con link al PR

#### Comentar en el PR:
1. Ir al PR
2. Agregar un comentario: `@skillberry-bot Esta función tiene SQL injection, usa prepared statements`
3. El workflow "Fix PR Reviews with Bob" se ejecutará
4. Bob corregirá el código automáticamente
5. Bob responderá al comentario explicando el fix

## 🔍 Troubleshooting

### Problema: Git push pide credenciales

**Solución 1: Usar Personal Access Token**
1. Ir a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Permisos: `repo` (full control)
4. Copiar token
5. Cuando git pida password, pegar el token

**Solución 2: Usar SSH**
```powershell
# Generar SSH key
ssh-keygen -t ed25519 -C "tu-email@example.com"

# Copiar public key
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard

# Agregar en GitHub: Settings → SSH and GPG keys → New SSH key
# Cambiar remote a SSH
git remote set-url origin git@github.com:TU-USUARIO/bob-cicd-automation-lab.git
```

### Problema: Workflow no se ejecuta

1. Verificar que el secret `BOBSHELL_API_KEY` existe:
   - Settings → Secrets and variables → Actions
2. Verificar permisos de workflows:
   - Settings → Actions → General → Workflow permissions
   - Seleccionar "Read and write permissions"
3. Ver logs del workflow:
   - Actions → Click en workflow → Click en job

### Problema: Bob no comenta en el PR

1. Verificar que BOBSHELL_API_KEY es válido
2. Verificar que el PR tiene el label correcto
3. Ver logs del workflow para errores
4. Verificar que el workflow tiene permisos de escritura

## 📊 Comandos Útiles de PowerShell

```powershell
# Ver status de git
git status

# Ver branches
git branch -a

# Ver commits
git log --oneline

# Ver remote
git remote -v

# Ver archivos staged
git diff --cached --name-only

# Ver último commit
git show HEAD

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Ver workflows (si instalas gh después)
gh workflow list
gh run list
gh pr list
gh issue list
```

## ✅ Checklist de Configuración

- [ ] Repositorio creado en GitHub
- [ ] Git inicializado localmente
- [ ] Remote configurado
- [ ] Rama main con código bueno pusheada
- [ ] Rama dev con código malo pusheada
- [ ] Secret BOBSHELL_API_KEY configurado
- [ ] Labels creados
- [ ] Pull Request creado
- [ ] Label "review-with-bob" agregado al PR
- [ ] Issues creados con label "fix-with-bob"
- [ ] Workflows ejecutándose
- [ ] Bob comentando en PR e issues

## 🎯 Próximos Pasos

1. ✅ Configuración completada
2. 🔄 Observar Bob en acción
3. 📸 Capturar screenshots de resultados
4. 📊 Documentar métricas
5. 🎓 Preparar presentación
6. 🚀 Compartir con el equipo

---

**¡Configuración Completa!** 🎉

Tu laboratorio está listo para demostrar cómo Bob Shell automatiza el ciclo de vida de desarrollo.