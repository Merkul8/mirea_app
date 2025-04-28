import {useLocation, useNavigate} from 'react-router-dom';
import {useState} from "react";
import {backendUrls} from "../../../Utils/urls.js";

function VerifyPage() {
    const location = useLocation();
    const {user_id} = location.state || {};

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        activation_code: '',
        user_id: user_id
    });
    console.log("USER_ID", user_id);

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);

        try {
            console.log("BODY", JSON.stringify(formData));
            const response = await fetch(backendUrls.varify, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка регистрации');
            }

            const data = await response.json();
            console.log('Успешная верификация:', data);
            navigate('/login');
        } catch (err) {
            console.error('Ошибка верификации:', err);
            setError(err.message || 'Произошла ошибка при верификации');
        } finally {
            setIsLoading(false);
        }
    };

    // Проверка наличия user_id
    if (!user_id) {
        return (<div>Ошибка: отсутствует user_id</div>);
    }

    return (
        <div className="register-container">
            <h2>Верификация</h2>
            <form onSubmit={handleSubmit} className="register-form">
                <div className="form-group">
                    <label>Код активации:</label>
                    <input
                        type="text"
                        name="activation_code"
                        value={formData.activation_code}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit" className="submit-btn">Проверить</button>
            </form>
        </div>
    );
}

export default VerifyPage;