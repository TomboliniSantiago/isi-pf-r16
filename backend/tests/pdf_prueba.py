"""Genera PDF mínimos con texto (sin dependencias) para probar la lectura de comprobantes digitales.

También lo usa db/generar_comprobantes_prueba.py para armar el conjunto de facturas de demostración.
"""


def _escapar(texto: str) -> bytes:
    crudo = texto.encode("cp1252", errors="replace")
    return crudo.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def pdf_con_texto(lineas: list[str]) -> bytes:
    """Una página A4 con cada línea en un renglón (Helvetica 10, codificación WinAnsi)."""
    flujo = (
        b"BT /F1 10 Tf 12 TL 50 800 Td\n" + b"".join(b"(" + _escapar(linea) + b") Tj T*\n" for linea in lineas) + b"ET"
    )
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(flujo)).encode() + b" >>\nstream\n" + flujo + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    salida = bytearray(b"%PDF-1.4\n")
    posiciones = []
    for numero, objeto in enumerate(objetos, start=1):
        posiciones.append(len(salida))
        salida += f"{numero} 0 obj\n".encode() + objeto + b"\nendobj\n"
    inicio_xref = len(salida)
    salida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode()
    salida += b"".join(f"{p:010d} 00000 n \n".encode() for p in posiciones)
    salida += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{inicio_xref}\n%%EOF\n".encode()
    return bytes(salida)


def factura_arca(
    *,
    letra: str = "A",
    codigo: str = "01",
    punto_venta: int = 3,
    numero: int = 1520,
    fecha: str = "05/11/2026",
    emisor: tuple[str, str] = ("Mayorista del Litoral S.A.", "30701234568"),
    receptor: tuple[str, str] = ("Distribuidora Andina S.A.", "30714582131"),
    neto: str = "1.000,00",
    iva: str = "210,00",
    otros: str = "0,00",
    total: str = "1.210,00",
) -> list[str]:
    """Líneas con el formato de una factura electrónica de ARCA."""
    return [
        "ORIGINAL",
        f"{letra}",
        f"FACTURA COD. {codigo}",
        f"Razón Social: {emisor[0]}",
        "Domicilio Comercial: Ruta 168 Km 3 - Santa Fe",
        "Condición frente al IVA: IVA Responsable Inscripto",
        f"Punto de Venta: {punto_venta:05d} Comp. Nro: {numero:08d}",
        f"Fecha de Emisión: {fecha}",
        f"CUIT: {emisor[1]}",
        "Ingresos Brutos: 921-123456-1",
        f"CUIT: {receptor[1]}",
        f"Apellido y Nombre / Razón Social: {receptor[0]}",
        "Condición frente al IVA: IVA Responsable Inscripto",
        "Condición de venta: Cuenta Corriente",
        "Código Producto / Servicio Cantidad U. Medida Precio Unit. Subtotal",
        f"Importe Neto Gravado: $ {neto}",
        f"IVA 21%: $ {iva}",
        f"Importe Otros Tributos: $ {otros}",
        f"Importe Total: $ {total}",
        "CAE N°: 76451234567890",
        "Fecha de Vto. de CAE: 15/11/2026",
    ]
