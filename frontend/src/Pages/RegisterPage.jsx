import RegisterForm from "../Components/Auth/RegisterForm/RegisterForm.jsx";
import '../Components/Auth/RegisterForm/RegisterForm.css';

export default function RegisterPage() {
    return (
        <div className="register-page">
            <div className="register-form-container">
                <RegisterForm/>
            </div>
        </div>
    );
}