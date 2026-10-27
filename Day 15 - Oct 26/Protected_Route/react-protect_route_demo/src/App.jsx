import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import About from "./pages/About";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        {/* basically it means Dashboard page is protected and the home and login are not */}
        {/* Write all your protected pages in the following section. */}

        <Route element={<ProtectedRoute />}>    
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about" element={<About/>}/>
        </Route>
        {/* Any other route is not present in our app, so show 404 not found error */}
        {/* Eg if user directly searches for /employees then it shows 404 */}
        <Route
          path="*"
          element={<h1>404 - Page Not Found</h1>}
        />
      </Routes>
    </AuthProvider>
  );
}
