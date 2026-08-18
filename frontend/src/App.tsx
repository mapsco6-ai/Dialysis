import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./auth/AuthContext";
import { ProtectedRoute } from "./auth/ProtectedRoute";
import { LoginPage } from "./pages/LoginPage";
import { ComingSoonPage } from "./pages/ComingSoonPage";
import { ReceptionDashboard } from "./pages/dashboard/ReceptionDashboard";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <ReceptionDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/patients"
              element={
                <ProtectedRoute>
                  <ComingSoonPage title="المرضى" />
                </ProtectedRoute>
              }
            />
            <Route
              path="/scheduling"
              element={
                <ProtectedRoute>
                  <ComingSoonPage title="الجدولة" />
                </ProtectedRoute>
              }
            />
            <Route
              path="/pharmacy"
              element={
                <ProtectedRoute>
                  <ComingSoonPage title="الصيدلية" />
                </ProtectedRoute>
              }
            />
            <Route
              path="/warehouse"
              element={
                <ProtectedRoute>
                  <ComingSoonPage title="المخزن" />
                </ProtectedRoute>
              }
            />
            <Route
              path="/nursing"
              element={
                <ProtectedRoute>
                  <ComingSoonPage title="مهام التمريض" />
                </ProtectedRoute>
              }
            />
            <Route
              path="/lab"
              element={
                <ProtectedRoute>
                  <ComingSoonPage title="المختبر" />
                </ProtectedRoute>
              }
            />
            <Route
              path="/staff"
              element={
                <ProtectedRoute>
                  <ComingSoonPage title="الموظفون" />
                </ProtectedRoute>
              }
            />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
