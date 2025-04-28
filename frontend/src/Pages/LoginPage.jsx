import LoginForm from "../Components/Auth/LoginForm/LoginForm.jsx";
import '../Components/Auth/RegisterForm/RegisterForm.css';

export default function LoginPage() {
    return (
        <div className="register-page" style={{marginLeft: "700px"}}>
            <div className="register-form-container">
                <LoginForm/>
            </div>
        </div>
    );
}