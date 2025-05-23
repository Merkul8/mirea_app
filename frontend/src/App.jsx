import { Routes, Route } from 'react-router-dom';
import RegisterPage from './Pages/RegisterPage.jsx';
import VerifyPage from './Pages/VerifyPage.jsx';
import LoginPage from './Pages/LoginPage.jsx';
// import MainPage from './Pages/MainPage.jsx';
import AccountPage from './Pages/AccountPage.jsx';
import DepartamentUsersPage from "./Pages/DepartamentUsers.jsx";
import DepUserRetrieve from "./Pages/DepUserRetrieve.jsx";
import DepartamentMetricsPage from "./Pages/DepartamentMetricPage.jsx";
import ProfileEditPage from "./Pages/ProfileEditPage.jsx";
import AdminPage from "./Pages/AdminPage.jsx";


export default function App() {

  return (
    <>
      <Routes>
        {/*<Route path="/" element={<MainPage />} />*/}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/verify" element={<VerifyPage />} />
        <Route path="/me" element={<AccountPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/users/departament" element={<DepartamentUsersPage />} />
        <Route path="/departament/metrics" element={<DepartamentMetricsPage />} />
        <Route path="/users/departament/:user_id" element={<DepUserRetrieve />} />
        <Route path="/profile/edit" element={<ProfileEditPage />} />
        {/*<Route path="*" element={<PageNotFound />} />*/}
      </Routes>
    </>
  )

}
