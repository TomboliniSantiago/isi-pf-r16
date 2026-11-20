interface Props {
  moneda: string | null;
  cotizacion: string | null;
}

/** Moneda de una compra o venta. Si el comprobante estaba en moneda extranjera, muestra la cotización
 * con la que se convirtió: los importes registrados siempre están en pesos. */
export function MonedaComprobante({ moneda, cotizacion }: Props) {
  if (!moneda) return <>—</>;
  if (moneda === "ARS") return <>Pesos (ARS)</>;
  const tasa = new Intl.NumberFormat("es-AR", { maximumFractionDigits: 6 }).format(Number(cotizacion ?? 0));
  return (
    <>
      {moneda} · cotización {tasa}{" "}
      <span className="texto-secundario">(importes convertidos a pesos)</span>
    </>
  );
}
