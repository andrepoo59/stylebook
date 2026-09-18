"""
Utilidades compartidas: exigir sesión activa (equivalente a exigirSesion()
en el ejemplo ManoLista, pero del lado del servidor con Flask).
"""
from functools import wraps
from flask import session, redirect, url_for, request, abort

from supabase_client import sb_como_usuario


def exigir_sesion(vista):
    """Redirige a /login si no hay sesión activa (HU-02)."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "access_token" not in session:
            return redirect(url_for("auth.login", volver=request.path))
        return vista(*args, **kwargs)
    return envoltura


def exigir_admin(vista):
    """Solo permite el acceso a cuentas con cargo de administrador."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "access_token" not in session:
            return redirect(url_for("auth.login", volver=request.path))
        if session.get("rol") != "admin":
            abort(403)
        return vista(*args, **kwargs)
    return envoltura


def cliente_sesion():
    """Cliente de Supabase autenticado como el usuario actual (para que apliquen las RLS)."""
    return sb_como_usuario(session["access_token"], session["refresh_token"])

