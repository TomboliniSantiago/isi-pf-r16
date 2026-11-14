"""Plantilla HTML de los correos que envía EugenIA.

Pensada para clientes de correo (Gmail, Outlook): maquetado con tablas y estilos en línea, sin CSS
externo ni bloques <style>. Todo lo que se interpola se escapa con html.escape.
"""

from html import escape

_FUENTE = "Segoe UI, Helvetica, Arial, sans-serif"
_FUENTE_MONO = "Consolas, 'Courier New', Courier, monospace"
_AZUL_OSCURO = "#0b1f3a"
_TEXTO = "#1e293b"
_GRIS = "#64748b"
_FONDO = "#eef2f7"


def plantilla_html(
    titulo: str,
    parrafos: list[str],
    codigo: str | None = None,
    vencimiento: str | None = None,
    aviso: str | None = None,
) -> str:
    """Devuelve el correo completo en HTML, listo para usarse como alternativa al texto plano.
    El vencimiento va después del código con el estilo de los párrafos; el aviso cierra en
    letra chica gris."""
    estilo_parrafo = f"font-family:{_FUENTE};font-size:15px;line-height:1.6;color:{_TEXTO};"
    bloques = [f'<p style="margin:0 0 16px 0;{estilo_parrafo}">{escape(parrafo)}</p>' for parrafo in parrafos]
    if codigo is not None:
        bloques.append(
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" '
            'style="margin:8px auto 24px auto;border-collapse:separate;">'
            f'<tr><td align="center" style="background-color:{_FONDO};border:1px solid #d6dee8;'
            'border-radius:8px;padding:16px 28px;">'
            f'<span style="font-family:{_FUENTE_MONO};font-size:32px;line-height:40px;font-weight:bold;'
            f'letter-spacing:8px;color:{_AZUL_OSCURO};">{escape(codigo)}</span>'
            "</td></tr></table>"
        )
    if vencimiento is not None:
        bloques.append(f'<p style="margin:0 0 16px 0;text-align:left;{estilo_parrafo}">{escape(vencimiento)}</p>')
    if aviso is not None:
        bloques.append(
            f'<p style="margin:0;font-family:{_FUENTE};font-size:13px;line-height:1.5;color:{_GRIS};">'
            f"{escape(aviso)}</p>"
        )
    contenido = "".join(bloques)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titulo)}</title>
</head>
<body style="margin:0;padding:0;background-color:{_FONDO};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{_FONDO};">
<tr><td align="center" style="padding:32px 16px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
 style="max-width:520px;background-color:#ffffff;border-radius:12px;border-collapse:separate;">
<tr><td style="background-color:{_AZUL_OSCURO};border-radius:12px 12px 0 0;padding:24px 32px;">
<div style="font-family:{_FUENTE};font-size:24px;line-height:30px;color:#ffffff;">Eugen<b>IA</b></div>
<div style="font-family:{_FUENTE};font-size:13px;line-height:18px;color:#cbd5e1;padding-top:4px;">
Gestión contable inteligente, trazable y segura.</div>
</td></tr>
<tr><td style="padding:32px;">
<h1 style="margin:0 0 8px 0;font-family:{_FUENTE};font-size:20px;line-height:28px;color:{_AZUL_OSCURO};">
{escape(titulo)}</h1>
{contenido}
</td></tr>
<tr><td style="border-top:1px solid #e2e8f0;padding:16px 32px;">
<p style="margin:0;font-family:{_FUENTE};font-size:11px;line-height:16px;color:{_GRIS};">
Este es un mensaje automático de EugenIA. No responda a este correo.</p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
"""
