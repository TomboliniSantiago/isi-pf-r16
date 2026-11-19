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
    return _pdf(flujo)


def pdf_por_caracter(lineas: list[str], avance: float = 7.5, interlineado: float = 12.75) -> bytes:
    """Como lo generan algunos sistemas de facturación que imitan una impresora: cada carácter con su propia
    posición en una grilla de ancho fijo y en su propio bloque BT/ET (la extracción estándar devuelve un
    carácter por renglón)."""
    instrucciones = [b"/F1 12 Tf\n"]
    for fila, linea in enumerate(lineas):
        y = 800 - fila * interlineado
        for columna, caracter in enumerate(linea):
            if caracter != " ":
                x = 20 + columna * avance
                # Igual que el generador real: Td al borde superior, Td relativo y escalado horizontal.
                instrucciones.append(
                    f"86.5 Tz BT 0 831 Td {x:.2f} {y - 831:.2f} Td (".encode()
                    + _escapar(caracter)
                    + b") Tj 100 Tz ET\n"
                )
    return _pdf(b"".join(instrucciones))


def _pdf(flujo: bytes) -> bytes:
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


def factura_preimpresa() -> list[str]:
    """Líneas de una factura de sistema propio (no la plantilla de ARCA): "Fecha:" con año de dos dígitos,
    fecha de inicio de actividades, SUB-TOTAL como neto, "IVA : 21.00" seguido del importe y TOTAL suelto.
    El nombre del emisor no figura en el texto (va en el logo). Datos ficticios."""
    return [
        "                                         A",
        "                                       Cod.001",
        "                                                            FACTURA",
        "                                                    Nº 00012-00004567",
        "Belgrano 450                                        Fecha: 04 / 09 / 26",
        "Santa Fe, República Argentina                C.U.I.T.: 30-70123456-8",
        "IVA RESPONSABLE INSCRIPTO                    Ing. Brutos Nº: 021-013864-9",
        "                                             Fecha Inicio Actividades: 15/05/1983",
        "Señor(es): DISTRIBUIDORA ANDINA S.A.               Cod. Cliente: 0ANDI",
        "IVA Responsable inscripto                    C.U.I.T. Nº: 30-71458213-1",
        "Condicion de Venta: CUENTA CORRIENTE         Remito:",
        "Cantidad   Codigo   Descripcion            Precio  Alicuota      Importe",
        "1.000      F851     SERVICIO DE CATERING   1000.00   21.00     1,000.00",
        "                    SUB-TOTAL                                 1,050.00",
        "                    DESC.     50.00",
        "                    SUB-TOTAL                                 1,000.00",
        "                    IVA :     21.00                             210.00",
        "                    TOTAL                                     1,210.00",
        "CAE: 76451234567890",
        "VTO: 14/09/2026",
    ]


def factura_en_dolares(
    *,
    punto_venta: int = 3,
    numero: int = 4512,
    cliente: tuple[str, str] = ("Comercial Santa Fe SRL", "30712345671"),
    neto: str = "28,172.00",
    iva: str = "5,916.12",
    total: str = "34,088.12",
    cotizacion: str = "1,545.50",
) -> list[str]:
    """Factura A en dólares con el modelo de la empresa piloto (Microsoft Print to PDF): importes con "u$s",
    moneda y cotización, código de cliente delante de la razón social y encabezado "IVA" de la tabla en un
    renglón propio. Emisor: la empresa de las pruebas (Distribuidora Andina S.A.). Datos ficticios."""
    return [
        "A   FACTURA",
        "Cod 01",
        "Fecha:  05/11/2026",
        f"Factura Nº:{punto_venta:05d}- {numero:08d}",
        "ORIGINAL",
        "Razón Social:Distribuidora Andina S.A.   C.U.I.T.: 30-71458213-1",
        "Domicilio:Ruta 168 Km 3 - Santa Fe   Ingresos Brutos:921-757800-2",
        "Fecha de Inicio de Actividades:05/12/2001",
        "Condición frente al IVA:Responsable Inscripto",
        f"Apellido y Nombre / Razón Social:00701 -    {cliente[0]}   C.U.I.T.: {cliente[1]}",
        "Domicilio:Bv. Pellegrini 1200   Condición frente al IVA:Responsable Inscripto",
        "Condición de venta:CONTADO   Orden de Compra:   Remito:",
        " Código     Producto / Servicio   Cantidad   U. medida   Precio Unit. % Bonif   Subtotal   Alicuota",
        "   IVA",
        "88497899  HERBICIDA X 10 LTS.   400.00   Lt   41.00   0.00 16,400.00 21.00    19,844.00",
        f"Vencimiento de Pago: 05/11/2026 u$s{total}",
        "Importe  expresado en:  Dólar   Importe No Gravado: u$s   0.00",
        f"Cotización:  {cotizacion}   Importe Exento: u$s   0.00",
        f"Importe Neto Gravado: u$s   {neto}",
        "IVA 27%: u$s   0.00",
        f"IVA 21%: u$s   {iva}",
        "IVA 10.5%: u$s   0.00",
        "Importe Otros Tributos: u$s   0.00",
        f"Importe Total: u$s   {total}",
        "CAE:  86440858279262",
        "Fecha Vto. Cae:  15/11/2026",
    ]
