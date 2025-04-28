import '../Components/Auth/RegisterForm/RegisterForm.css';
import VerifyForm from "../Components/Auth/VerifyForm/VerifyForm.jsx";


export default function VerifyPage() {
    return (
        <div className="register-page" style={{marginLeft: "750px"}}>
            <div className="register-form-container">
                <VerifyForm/>
            </div>
        </div>
    );
}