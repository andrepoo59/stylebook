# StyleBook — Sprint 1

Plataforma web para un salón de belleza + barbería: catálogo de servicios,
profesionales y reserva de citas. Este Sprint 1 cubre las historias de
usuario **HU-01 a HU-07** (base de usuarios, profesionales y catálogo de
servicios). Las historias de reservas (HU-08 en adelante) quedan para los
siguientes sprints.

**Stack:** Python + Flask (backend y vistas) + Supabase (base de datos,
autenticación y seguridad a nivel de fila).

## Historias de usuario incluidas

| HU | Historia | Dónde vive |
|----|----------|------------|
| HU-01 | Registro de usuario | `blueprints/auth.py` → `/registro` |
| HU-02 | Inicio de sesión | `blueprints/auth.py` → `/login` |
| HU-03 | Gestión del perfil | `blueprints/perfil.py` → `/perfil` |
| HU-04 | Registro de profesional | `blueprints/profesionales.py` → `/profesionales/registro` |
| HU-05 | Gestión de servicios | `blueprints/servicios.py` → `/mis-servicios` |
| HU-06 | Consultar servicios | `blueprints/servicios.py` → `/servicios` |
| HU-07 | Consultar profesional | `blueprints/profesionales.py` → `/profesionales` |

## 1. Crear el proyecto en Supabase

1. Entra a [supabase.com](https://supabase.com) y crea un proyecto nuevo.
2. Ve a **SQL Editor** y pega completo el contenido de `db/schema.sql`. Ejecútalo
   (`Run`). Esto crea las tablas `perfiles`, `profesionales`, `servicios`, el
   trigger que crea el perfil automáticamente al registrarse, y las políticas
   de seguridad (RLS).
3. Ve a **Project Settings → API** y copia:
   - `Project URL` → será tu `SUPABASE_URL`
   - `anon public key` → será tu `SUPABASE_ANON_KEY`

## 2. Configurar el proyecto localmente

```bash
# 1. Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env       # Windows
cp .env.example .env         # macOS / Linux
```

Abre `.env` y pega tus credenciales reales de Supabase.

## 3. Ejecutar

```bash
python app.py
```

Abre `http://localhost:5000` en el navegador.

## Estructura del proyecto

```
stylebook/
├── app.py                  # Punto de entrada, registra los blueprints
├── supabase_client.py      # Cliente único de Supabase
├── utilidades.py           # Decorador de sesión, cliente autenticado por usuario
├── requirements.txt
├── .env.example
├── db/
│   └── schema.sql          # Tablas, trigger y políticas RLS
├── blueprints/
│   ├── auth.py             # HU-01, HU-02
│   ├── perfil.py           # HU-03
│   ├── profesionales.py    # HU-04, HU-07
│   └── servicios.py        # HU-05, HU-06
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   ├── perfil/
│   ├── profesionales/
│   └── servicios/
└── static/
    └── css/estilos.css
```

## Cargos de cuenta

StyleBook maneja tres cargos, guardados en `perfiles.rol`:

- **Cliente**: puede reservar citas (a partir del próximo sprint) y consultar el catálogo. Es el cargo por defecto.
- **Profesional / Local**: se elige en el registro, o desde "Registrarme como profesional" en el perfil. Su ficha queda en estado `pendiente` hasta que un administrador la aprueba (`/admin`); solo entonces aparece en el listado público (HU-07) y en el catálogo (HU-06).
- **Administrador**: aprueba o rechaza a los profesionales desde `/admin`. Por seguridad, este cargo **no se auto-asigna** en el formulario público de registro — hay que asignarlo manualmente.

### Cómo asignar el cargo de administrador

En el **SQL Editor** de Supabase, después de que la persona ya se haya registrado normalmente como cliente:

```sql
update public.perfiles set rol = 'admin' where id = (
  select id from auth.users where email = 'correo-del-administrador@ejemplo.com'
);
```

## Notas de diseño

- La sesión de Flask guarda el `access_token` y `refresh_token` que entrega
  Supabase Auth al iniciar sesión (HU-02). Cada operación que debe respetar
  las políticas RLS (perfil propio, servicios propios) usa un cliente de
  Supabase autenticado con esos tokens (`cliente_sesion()` en `utilidades.py`),
  no el cliente anónimo.
- El registro de profesional (HU-04) y la aprobación de su cuenta quedan en
  estado `aprobado` automáticamente en este sprint; el flujo de moderación
  manual por el administrador del negocio puede activarse en un sprint
  posterior sin cambiar el esquema.
- El catálogo de servicios (HU-06) admite filtro opcional por categoría vía
  `?categoria=...`.
