from app.plantilla_correo import plantilla_html


def test_incluye_titulo_y_codigo():
    salida = plantilla_html("Código de inicio de sesión", ["Use el siguiente código:"], codigo="123456", aviso="Vence")
    assert "Código de inicio de sesión" in salida
    assert "123456" in salida
    assert "Use el siguiente código:" in salida
    assert "No responda a este correo." in salida


def test_escapa_caracteres_html():
    salida = plantilla_html("<b>Título</b>", ['<script>alert("x")</script>'], codigo="<1&2>", aviso="a & b")
    assert "<script>" not in salida
    assert "<b>Título</b>" not in salida
    assert "&lt;b&gt;Título&lt;/b&gt;" in salida
    assert "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;" in salida
    assert "&lt;1&amp;2&gt;" in salida
    assert "a &amp; b" in salida


def test_orden_de_bloques_hasta_el_pie():
    salida = plantilla_html("T", ["P"], codigo="123456", vencimiento="Vence", aviso="Si usted no")
    assert (
        salida.index("123456")
        < salida.index("Vence")
        < salida.index("Si usted no")
        < salida.index("No responda a este correo.")
    )


def test_sin_codigo_ni_aviso():
    salida = plantilla_html("Aviso", ["Texto"])
    assert "letter-spacing" not in salida
    assert "Gracias" not in salida
