import { BrowserRouter } from "react-router-dom"
import { AuthProvider } from "./context/authcontext"
import AppRoutes from "./Routes/approute"

function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  )
}

export default App