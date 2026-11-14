import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import { RutaProtegida } from "./auth/RutaProtegida";
import { Layout } from "./components/Layout";
import { CambiarPasswordPage } from "./pages/CambiarPasswordPage";
import { ClientesPage } from "./pages/clientes/ClientesPage";
import { ComprasPage } from "./pages/compras/ComprasPage";
import { DevUsuariosPage } from "./pages/DevUsuariosPage";
import { DocumentosPage } from "./pages/documentos/DocumentosPage";
import { InicioPage } from "./pages/InicioPage";
import { LibroDiarioPage } from "./pages/libro-diario/LibroDiarioPage";
import { LibroMayorPage } from "./pages/libro-mayor/LibroMayorPage";
import { LoginPage } from "./pages/LoginPage";
import { PlanCuentasPage } from "./pages/plan-cuentas/PlanCuentasPage";
import { ProveedoresPage } from "./pages/proveedores/ProveedoresPage";
import { RecuperarPasswordPage } from "./pages/RecuperarPasswordPage";
import { SinPermisoPage } from "./pages/SinPermisoPage";
import { UsuariosPage } from "./pages/UsuariosPage";
import { VentasPage } from "./pages/ventas/VentasPage";

export function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/recuperar-password" element={<RecuperarPasswordPage />} />
          <Route path="/dev/usuarios" element={<DevUsuariosPage />} />
          <Route
            path="/cambiar-password"
            element={
              <RutaProtegida>
                <CambiarPasswordPage />
              </RutaProtegida>
            }
          />
          <Route
            element={
              <RutaProtegida>
                <Layout />
              </RutaProtegida>
            }
          >
            <Route index element={<InicioPage />} />
            <Route path="plan-cuentas" element={<PlanCuentasPage />} />
            <Route path="libro-diario" element={<LibroDiarioPage />} />
            <Route path="libro-mayor" element={<LibroMayorPage />} />
            <Route path="clientes" element={<ClientesPage />} />
            <Route path="proveedores" element={<ProveedoresPage />} />
            <Route path="ventas" element={<VentasPage />} />
            <Route path="compras" element={<ComprasPage />} />
            <Route path="comprobantes-digitales" element={<DocumentosPage />} />
            <Route
              path="usuarios"
              element={
                <RutaProtegida roles={["ADMINISTRADOR"]}>
                  <UsuariosPage />
                </RutaProtegida>
              }
            />
            <Route path="sin-permiso" element={<SinPermisoPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
