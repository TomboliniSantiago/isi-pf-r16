import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import { RutaProtegida } from "./auth/RutaProtegida";
import { Layout } from "./components/Layout";
import { CambiarPasswordPage } from "./pages/CambiarPasswordPage";
import { InicioPage } from "./pages/InicioPage";
import { LoginPage } from "./pages/LoginPage";
import { SinPermisoPage } from "./pages/SinPermisoPage";
import { UsuariosPage } from "./pages/UsuariosPage";

export function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
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
