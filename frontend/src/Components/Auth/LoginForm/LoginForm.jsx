import {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {backendUrls} from "../../../Utils/urls.js"; // Подключаем стили
import '../RegisterForm/RegisterForm.css'

const LoginForm = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(backendUrls.login, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка аутентификации');
            }

            const data = await response.json();
            console.log('Успешная авторизация:', data);

            if (data.user?.is_admin) {
                navigate('/admin'); // Если суперадмин — на админку
            } else {
                navigate('/me'); // Иначе — на профиль
            }

        } catch (err) {
            console.error('Ошибка авторизации:', err);
            setError(err.message || 'Произошла ошибка при авторизации');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="register-container">
            <h2>Авторизация</h2>
            <form onSubmit={handleSubmit} className="register-form">
                <div className="form-group">
                    <label>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Пароль:</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>

                <button type="submit" className="submit-btn">Войти</button>
            </form>
        </div>
    );
};

export default LoginForm;