import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import './RegisterForm.css';
import {backendUrls} from "../../../Utils/urls.js"; // Подключаем стили

const RegisterForm = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        patronymic: '',
        elibrary_id: '',
        role: '',
        work_type: '',
        post: '',
        academic_degree: '',
        departament_id: ''
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
            const response = await fetch(backendUrls.register, {
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
            console.log('Успешная регистрация:', data);
            navigate('/verify', {
                state: {
                    user_id: data.user_id,
                }
            }); // Перенаправление после успеха
        } catch (err) {
            console.error('Ошибка регистрации:', err);
            setError(err.message || 'Произошла ошибка при регистрации');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="register-container">
            <h2>Регистрация</h2>
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

                <div className="name-fields">
                    <div className="form-group">
                        <label>Фамилия:</label>
                        <input
                            type="text"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Имя:</label>
                        <input
                            type="text"
                            name="first_name"
                            value={formData.first_name}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Отчество:</label>
                        <input
                            type="text"
                            name="patronymic"
                            value={formData.patronymic}
                            onChange={handleChange}
                            required
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label>ID в elibrary:</label>
                    <input
                        type="number"
                        name="elibrary_id"
                        value={formData.elibrary_id}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Роль:</label>
                    <select
                        name="role"
                        value={formData.role}
                        onChange={handleChange}
                        required
                    >
                        <option value="boss">boss</option>
                        <option value="teacher">teacher</option>
                        <option value="admin">admin</option>
                        <option value="assistant">assistant</option>
                        <option value="student">student</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Тип трудоустройства:</label>
                    <select
                        name="work_type"
                        value={formData.work_type}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Выберите тип</option>
                        <option value="Основное">Основное</option>
                        <option value="Совместительство">Совместительство</option>
                        <option value="Почасовик">Почасовик</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>Должность:</label>
                    <input
                        type="text"
                        name="post"
                        value={formData.post}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Учёная степень:</label>
                    <select
                        name="academic_degree"
                        value={formData.academic_degree}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Выберите степень</option>
                        <option value="Кандидат наук">Кандидат наук</option>
                        <option value="Доктор наук">Доктор наук</option>
                        <option value="Нет степени">Нет степени</option>
                    </select>
                </div>

                <div className="form-group">
                    <label>ID кафедры:</label>
                    <input
                        type="number"
                        name="departament_id"
                        value={formData.departament_id}
                        onChange={handleChange}
                        required
                    />
                </div>

                <button type="submit" className="submit-btn">Зарегистрироваться</button>
            </form>
        </div>
    );
};

export default RegisterForm;