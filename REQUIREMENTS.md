# Requisitos para Integración de Bob Shell en CI/CD

## Requisitos Obligatorios

### 1. API Key de Bob Shell
**Costo**: Requiere cuenta de IBM watsonx Code Assistant
- Obtener API key desde: https://bob.ibm.com
- La API key debe configurarse como secret en GitHub: `BOBSHELL_API_KEY`
- **IMPORTANTE**: Bob Shell es un producto de IBM que requiere licencia comercial

### 2. GitHub Actions
**Costo**: Depende del tipo de cuenta

#### Repositorios Públicos
- ✅ **GRATIS**: GitHub Actions es completamente gratuito para repositorios públicos
- Minutos ilimitados de ejecución
- No requiere cuenta pagada de GitHub

#### Repositorios Privados
Límites según el plan de GitHub:

| Plan | Minutos Gratis/Mes | Costo Adicional |
|------|-------------------|-----------------|
| **Free** | 2,000 minutos | $0.008/minuto |
| **Pro** | 3,000 minutos | $0.008/minuto |
| **Team** | 3,000 minutos | $0.008/minuto |
| **Enterprise** | 50,000 minutos | $0.008/minuto |

**Estimación de Uso**:
- Review de PR: ~5-10 minutos por ejecución
- Fix de Issues: ~10-15 minutos por ejecución
- Con 2,000 minutos gratis puedes hacer ~200-400 reviews/mes

### 3. GitHub Token (Opcional pero Recomendado)
**Costo**: Gratis

Para operaciones avanzadas (crear PRs, comentar, etc.):
- Crear Personal Access Token (PAT) o usar GitHub App
- Configurar como secret: `GITHUB_TOKEN` o `SKILLBERRY_BOT_TOKEN`
- Permisos necesarios:
  - `repo` (acceso completo al repositorio)
  - `workflow` (actualizar workflows)
  - `write:packages` (si usas GitHub Packages)

## Requisitos Opcionales

### 4. CodeQL (Análisis de Seguridad)
**Costo**: Gratis para repositorios públicos

- **Repositorios Públicos**: Completamente gratis
- **Repositorios Privados**: 
  - Requiere GitHub Advanced Security
  - Incluido en GitHub Enterprise Cloud
  - $49/usuario/mes para otros planes

### 5. Runners de GitHub Actions
**Costo**: Depende del tipo

#### GitHub-hosted Runners (Recomendado para empezar)
- **Incluido** en los minutos gratuitos mencionados arriba
- Especificaciones:
  - 2-core CPU
  - 7 GB RAM
  - 14 GB SSD

#### Self-hosted Runners (Opcional)
- **Gratis** (usas tu propia infraestructura)
- Ventajas:
  - Sin límite de minutos
  - Mayor control
  - Puede ser más rápido
- Desventajas:
  - Requiere mantenimiento
  - Costos de infraestructura

## Resumen de Costos

### Escenario Mínimo (Repositorio Público)
```
✅ GitHub Actions: GRATIS
✅ CodeQL: GRATIS
❌ Bob Shell API: REQUIERE LICENCIA IBM
---
Total: Solo costo de licencia IBM watsonx Code Assistant
```

### Escenario Mínimo (Repositorio Privado - Plan Free)
```
✅ GitHub Actions: 2,000 minutos/mes GRATIS
✅ GitHub Token: GRATIS
❌ Bob Shell API: REQUIERE LICENCIA IBM
❌ CodeQL: Requiere GitHub Advanced Security ($49/usuario/mes)
---
Total: Licencia IBM + posible costo de Advanced Security
```

### Escenario Recomendado (Repositorio Privado - Plan Team)
```
✅ GitHub Actions: 3,000 minutos/mes incluidos
✅ GitHub Token: GRATIS
❌ Bob Shell API: REQUIERE LICENCIA IBM
✅ CodeQL: Incluido con Advanced Security
---
Costo mensual: $4/usuario (GitHub Team) + $49/usuario (Advanced Security) + Licencia IBM
```

## Configuración Paso a Paso

### Paso 1: Obtener Bob Shell API Key
1. Registrarse en IBM watsonx Code Assistant
2. Ir a https://bob.ibm.com
3. Generar API key desde el dashboard
4. Guardar la API key de forma segura

### Paso 2: Configurar Secrets en GitHub
1. Ir a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Agregar secrets:
   ```
   BOBSHELL_API_KEY = tu-api-key-de-bob
   GITHUB_TOKEN = tu-personal-access-token (opcional)
   ```

### Paso 3: Crear Labels en GitHub
```bash
gh label create "review-with-bob" --color "0E8A16" --description "Trigger Bob code review"
gh label create "fix-with-bob" --color "D93F0B" --description "Trigger Bob to fix issues"
```

### Paso 4: Verificar Workflows
Los workflows ya están configurados en `.github/workflows/`:
- `review-pr-with-skills.yml` - Review automático de PRs
- `fix-pr-reviews-with-bob.yml` - Fix de comentarios de review
- `fix-issues-with-bob.yml` - Fix de issues
- `codeql-with-bob-explanation.yml` - Análisis de seguridad con CodeQL

### Paso 5: Probar la Integración
```bash
# 1. Crear un PR de prueba
git checkout -b test-bob-integration
echo "test" > test.txt
git add test.txt
git commit -m "Test Bob integration"
git push origin test-bob-integration
gh pr create --title "Test Bob" --body "Testing Bob integration"

# 2. Agregar label para activar review
gh pr edit <PR_NUMBER> --add-label "review-with-bob"

# 3. Verificar que el workflow se ejecuta
gh run list --workflow=review-pr-with-skills.yml
```

## Preguntas Frecuentes

### ¿Necesito cuenta pagada de GitHub?
**NO** para repositorios públicos. Los 2,000 minutos gratis del plan Free son suficientes para empezar con repositorios privados.

### ¿Cuánto cuesta Bob Shell?
Bob Shell es parte de IBM watsonx Code Assistant. Debes contactar a IBM para precios empresariales. No hay plan gratuito público.

### ¿Puedo usar esto sin Bob Shell?
NO. Los workflows están diseñados específicamente para Bob Shell. Sin la API key de Bob, los workflows fallarán.

### ¿Funciona con Bitbucket o GitLab?
Los workflows actuales son específicos para GitHub Actions. Para Bitbucket Pipelines o GitLab CI/CD, necesitarías adaptar los workflows.

### ¿Qué pasa si me quedo sin minutos de GitHub Actions?
- **Opción 1**: Comprar minutos adicionales ($0.008/minuto)
- **Opción 2**: Actualizar a un plan superior
- **Opción 3**: Usar self-hosted runners (gratis pero requiere infraestructura)

## Alternativas y Consideraciones

### Si no tienes licencia de Bob Shell
Considera estas alternativas:
1. **GitHub Copilot** - $10/mes por usuario
2. **SonarQube** - Análisis de código gratuito (Community Edition)
3. **CodeRabbit** - Review automático de PRs
4. **Conventional review tools** - ESLint, Prettier, etc.

### Optimización de Costos
1. **Usar repositorios públicos** cuando sea posible (todo gratis)
2. **Limitar ejecuciones** con condiciones en workflows
3. **Usar caching** para reducir tiempo de ejecución
4. **Self-hosted runners** para proyectos grandes

## Contacto y Soporte

- **Bob Shell**: https://bob.ibm.com
- **IBM watsonx**: https://www.ibm.com/watsonx
- **GitHub Actions**: https://docs.github.com/actions
- **GitHub Advanced Security**: https://docs.github.com/code-security