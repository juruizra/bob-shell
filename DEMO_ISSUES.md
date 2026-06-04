# Issues de Ejemplo para Demo

Este documento contiene issues de ejemplo que puedes crear en GitHub para demostrar los workflows de Bob Shell.

## 📋 Cómo Usar

Para cada issue:
1. Copia el título y descripción
2. Crea el issue en GitHub: `gh issue create --title "..." --body "..."`
3. Agrega el label correspondiente
4. Observa cómo Bob responde automáticamente

---

## Issue 1: SQL Injection en Login

### Título
```
Login permite SQL injection en autenticación
```

### Descripción
```markdown
## Descripción del Problema
El método `login()` en `demo-app-bad/auth/login_bad.py` línea 38 construye queries SQL usando concatenación de strings, lo que permite ataques de SQL injection.

## Código Vulnerable
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

## Impacto
- **Severidad**: Critical
- Un atacante puede:
  - Bypassear autenticación usando `' OR '1'='1`
  - Extraer datos de la base de datos
  - Modificar o eliminar datos

## Solución Esperada
Usar prepared statements con parámetros:
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
result = cursor.execute(query, (username, password))
```

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `security`
- `critical`
- `fix-with-bob`
```

### Comando
```bash
gh issue create \
  --title "Login permite SQL injection en autenticación" \
  --body "$(cat <<'EOF'
## Descripción del Problema
El método login() en demo-app-bad/auth/login_bad.py línea 38 construye queries SQL usando concatenación de strings.

## Código Vulnerable
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

## Impacto
- Severidad: Critical
- Permite bypass de autenticación
- Extracción de datos

## Solución
Usar prepared statements con parámetros.
EOF
)" \
  --label "security,critical,fix-with-bob"
```

---

## Issue 2: Credenciales Hardcodeadas

### Título
```
Credenciales hardcodeadas en código fuente
```

### Descripción
```markdown
## Descripción del Problema
El archivo `demo-app-bad/auth/login_bad.py` contiene credenciales hardcodeadas en las líneas 10-12:

```python
ADMIN_PASSWORD = "admin123"
SECRET_KEY = "my-secret-key-12345"
```

## Impacto
- **Severidad**: Critical
- Credenciales expuestas en repositorio
- Riesgo de acceso no autorizado
- Violación de políticas de seguridad

## Solución Esperada
1. Mover credenciales a variables de entorno
2. Usar gestión de secretos (HashiCorp Vault, AWS Secrets Manager)
3. Agregar `.env` al `.gitignore`

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `security`
- `critical`
- `fix-with-bob`
```

---

## Issue 3: Violación de Principio de Responsabilidad Única

### Título
```
Clase LoginManager viola Single Responsibility Principle
```

### Descripción
```markdown
## Descripción del Problema
La clase `LoginManager` en `demo-app-bad/auth/login_bad.py` tiene demasiadas responsabilidades:
- Gestión de base de datos
- Autenticación
- Gestión de sesiones
- Logging
- Validación

## Código Problemático
```python
class LoginManager:
    # Hace TODO: DB, auth, sessions, logging, validation
```

## Impacto
- **Severidad**: High
- Difícil de mantener
- Difícil de testear
- Alto acoplamiento
- Viola SOLID principles

## Solución Esperada
Separar en clases especializadas:
- `DatabaseManager` - Solo gestión de BD
- `AuthenticationService` - Solo autenticación
- `SessionManager` - Solo sesiones
- `InputValidator` - Solo validación

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `architecture`
- `refactoring`
- `fix-with-bob`
```

---

## Issue 4: Logging de Datos Sensibles

### Título
```
Sistema logea passwords en texto plano
```

### Descripción
```markdown
## Descripción del Problema
El código logea passwords y datos sensibles en texto plano (líneas 41, 119):

```python
print(f"Login attempt: {username} with password: {password}")
print(f"New user registered: {username}, password: {password}, email: {email}")
```

## Impacto
- **Severidad**: High
- Exposición de credenciales en logs
- Violación de GDPR/compliance
- Riesgo de filtración de datos

## Solución Esperada
1. Nunca loggear passwords
2. Loggear solo información no sensible
3. Usar niveles de log apropiados
4. Implementar log sanitization

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `security`
- `compliance`
- `fix-with-bob`
```

---

## Issue 5: Funciones Demasiado Largas

### Título
```
Método register_user tiene más de 100 líneas
```

### Descripción
```markdown
## Descripción del Problema
El método `register_user()` tiene más de 100 líneas y hace demasiadas cosas.

## Impacto
- **Severidad**: Medium
- Difícil de leer y entender
- Difícil de testear
- Alto riesgo de bugs
- Viola principios de clean code

## Solución Esperada
Refactorizar en funciones más pequeñas:
- `validate_user_input()`
- `hash_password()`
- `save_user_to_db()`
- `log_registration()`

Cada función debe tener < 50 líneas.

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `code-quality`
- `refactoring`
- `fix-with-bob`
```

---

## Issue 6: Nombres de Variables Confusos

### Título
```
Variables con nombres no descriptivos (x, data, temp)
```

### Descripción
```markdown
## Descripción del Problema
El código usa nombres de variables confusos:
- `self.x` (línea 26)
- `self.data` (línea 27)
- `self.temp` (línea 28)
- `u, p` en parámetros (línea 186)

## Impacto
- **Severidad**: Low
- Código difícil de entender
- Mantenimiento complicado
- Onboarding lento para nuevos developers

## Solución Esperada
Usar nombres descriptivos:
- `x` → `login_status` o `is_authenticated`
- `data` → `user_cache` o `session_data`
- `temp` → `current_username`
- `u, p` → `username, password`

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `code-quality`
- `documentation`
- `fix-with-bob`
```

---

## Issue 7: Código Duplicado

### Título
```
Métodos login() y check_user() tienen lógica duplicada
```

### Descripción
```markdown
## Descripción del Problema
Los métodos `login()` y `check_user()` tienen lógica duplicada para consultar usuarios.

## Código Duplicado
Ambos métodos hacen queries similares a la tabla users.

## Impacto
- **Severidad**: Medium
- Viola DRY principle
- Cambios deben hacerse en múltiples lugares
- Mayor riesgo de inconsistencias

## Solución Esperada
Extraer lógica común a método privado:
```python
def _get_user_by_username(self, username):
    # Lógica compartida
```

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `code-quality`
- `refactoring`
- `fix-with-bob`
```

---

## Issue 8: Sin Validación de Entrada

### Título
```
Falta validación de entrada en todos los métodos
```

### Descripción
```markdown
## Descripción del Problema
Ningún método valida la entrada del usuario antes de procesarla.

## Impacto
- **Severidad**: High
- Permite ataques de injection
- Datos inválidos en base de datos
- Crashes inesperados

## Solución Esperada
Implementar validación:
- Username: 3-20 caracteres alfanuméricos
- Password: mínimo 8 caracteres, complejidad
- Email: formato válido
- Sanitización de todos los inputs

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `security`
- `validation`
- `fix-with-bob`
```

---

## Issue 9: Sin Manejo de Errores

### Título
```
Métodos no manejan errores apropiadamente
```

### Descripción
```markdown
## Descripción del Problema
El código usa `except Exception` genérico y expone errores internos.

## Código Problemático
```python
except Exception as e:
    print(f"Error: {e}")  # Expone detalles internos
```

## Impacto
- **Severidad**: Medium
- Información sensible expuesta
- Difícil debugging
- Mala experiencia de usuario

## Solución Esperada
1. Capturar excepciones específicas
2. Loggear errores apropiadamente
3. Retornar mensajes user-friendly
4. No exponer stack traces

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `bug`
- `error-handling`
- `fix-with-bob`
```

---

## Issue 10: Sin Rate Limiting

### Título
```
Login no implementa rate limiting ni account lockout
```

### Descripción
```markdown
## Descripción del Problema
El sistema permite intentos ilimitados de login sin:
- Rate limiting
- Account lockout después de X intentos fallidos
- CAPTCHA después de múltiples fallos

## Impacto
- **Severidad**: High
- Vulnerable a brute force attacks
- Vulnerable a credential stuffing
- No cumple con security best practices

## Solución Esperada
Implementar:
1. Máximo 5 intentos fallidos
2. Lockout de 15 minutos después de 5 fallos
3. Rate limiting por IP
4. Logging de intentos fallidos

## Archivos Afectados
- `demo-app-bad/auth/login_bad.py`

## Labels
- `security`
- `enhancement`
- `fix-with-bob`
```

---

## 🚀 Crear Todos los Issues Automáticamente

```bash
#!/bin/bash

# Issue 1
gh issue create --title "Login permite SQL injection en autenticación" \
  --body "El método login() construye queries SQL con concatenación de strings. Severidad: Critical" \
  --label "security,critical,fix-with-bob"

# Issue 2
gh issue create --title "Credenciales hardcodeadas en código fuente" \
  --body "ADMIN_PASSWORD y SECRET_KEY están hardcodeados. Severidad: Critical" \
  --label "security,critical,fix-with-bob"

# Issue 3
gh issue create --title "Clase LoginManager viola Single Responsibility Principle" \
  --body "LoginManager hace demasiadas cosas: DB, auth, sessions, logging. Severidad: High" \
  --label "architecture,refactoring,fix-with-bob"

# Issue 4
gh issue create --title "Sistema logea passwords en texto plano" \
  --body "Passwords se loggean en texto plano en múltiples lugares. Severidad: High" \
  --label "security,compliance,fix-with-bob"

# Issue 5
gh issue create --title "Método register_user tiene más de 100 líneas" \
  --body "Función demasiado larga, difícil de mantener. Severidad: Medium" \
  --label "code-quality,refactoring,fix-with-bob"

# Issue 6
gh issue create --title "Variables con nombres no descriptivos" \
  --body "Variables x, data, temp no son descriptivas. Severidad: Low" \
  --label "code-quality,documentation,fix-with-bob"

# Issue 7
gh issue create --title "Métodos login() y check_user() tienen lógica duplicada" \
  --body "Código duplicado viola DRY principle. Severidad: Medium" \
  --label "code-quality,refactoring,fix-with-bob"

# Issue 8
gh issue create --title "Falta validación de entrada en todos los métodos" \
  --body "Sin validación de inputs permite ataques. Severidad: High" \
  --label "security,validation,fix-with-bob"

# Issue 9
gh issue create --title "Métodos no manejan errores apropiadamente" \
  --body "Usa except Exception genérico y expone errores. Severidad: Medium" \
  --label "bug,error-handling,fix-with-bob"

# Issue 10
gh issue create --title "Login no implementa rate limiting ni account lockout" \
  --body "Vulnerable a brute force attacks. Severidad: High" \
  --label "security,enhancement,fix-with-bob"

echo "✅ 10 issues creados exitosamente"
```

---

## 📊 Resumen de Issues

| # | Título | Severidad | Categoría | Label |
|---|--------|-----------|-----------|-------|
| 1 | SQL Injection en Login | Critical | Security | fix-with-bob |
| 2 | Credenciales Hardcodeadas | Critical | Security | fix-with-bob |
| 3 | Violación SRP | High | Architecture | fix-with-bob |
| 4 | Logging de Passwords | High | Security | fix-with-bob |
| 5 | Funciones Largas | Medium | Code Quality | fix-with-bob |
| 6 | Nombres Confusos | Low | Code Quality | fix-with-bob |
| 7 | Código Duplicado | Medium | Code Quality | fix-with-bob |
| 8 | Sin Validación | High | Security | fix-with-bob |
| 9 | Sin Manejo de Errores | Medium | Bug | fix-with-bob |
| 10 | Sin Rate Limiting | High | Security | fix-with-bob |

**Total**: 10 issues que Bob puede resolver automáticamente