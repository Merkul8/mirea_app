import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { backendUrls } from "../Utils/urls.js";
import '../Components/Auth/Profile/Profile.css'

export default function ProfileEditPage() {
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        patronymic: "",
        elibrary_id: "",
        work_type: "",
        post: "",
        academic_degree: "",
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch(backendUrls.me, {
                    credentials: 'include',
                });

                if (!response.ok) {
                    throw new Error('Ошибка загрузки данных пользователя');
                }

                const data = await response.json();
                setFormData({
                    first_name: data.name || "",
                    last_name: data.last_name || "",
                    patronymic: data.patronymic || "",
                    elibrary_id: data.elibrary_id || "",
                    work_type: data.work_type || "",
                    post: data.post || "",
                    academic_degree: data.academic_degree || "",
                });
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(backendUrls.updateUser, {
                method: "PUT",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                alert("Профиль успешно обновлен!");
                navigate("/me");
            } else {
                const errorData = await response.json();
                alert(`Ошибка обновления профиля: ${errorData.message || "Неизвестная ошибка"}`);
            }
        } catch (err) {
            console.error("Ошибка при отправке формы:", err);
            alert("Ошибка отправки формы");
        }
    };

    if (loading) return <div className="loading">Загрузка...</div>;
    if (error) return <div className="error">Ошибка: {error}</div>;

    return (
        <div className="profile-edit-container">
            <h2>Редактировать профиль</h2>
            <form onSubmit={handleSubmit} className="profile-edit-form">
                <label>Имя:</label>
                <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} required />

                <label>Фамилия:</label>
                <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} required />

                <label>Отчество:</label>
                <input type="text" name="patronymic" value={formData.patronymic} onChange={handleChange} required />

                <label>ELIBRARY ID:</label>
                <input type="number" name="elibrary_id" value={formData.elibrary_id} onChange={handleChange} required />

                <label>Тип работы:</label>
                <input type="text" name="work_type" value={formData.work_type} onChange={handleChange} required />

                <label>Должность:</label>
                <input type="text" name="post" value={formData.post} onChange={handleChange} required />

                <label>Учёная степень:</label>
                <input type="text" name="academic_degree" value={formData.academic_degree} onChange={handleChange} required />

                <div className="btns">
                    <button type="submit" className="edit-btn">Сохранить изменения</button>
                    <button type="button" className="cancel-btn" onClick={() => navigate("/profile")}>Отмена</button>
                </div>
            </form>
        </div>
    );
}
