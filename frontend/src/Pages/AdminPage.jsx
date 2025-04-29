import {useEffect, useState} from "react";
import {backendUrls} from "../Utils/urls";
import "../Components/Auth/Account/Account.css";
import {useNavigate} from "react-router-dom";

export default function AdminPage() {
    const [adminData, setAdminData] = useState(null);
    const [usersToActivate, setUsersToActivate] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const adminRes = await fetch(backendUrls.me, {
                    credentials: 'include',
                });
                if (!adminRes.ok) throw new Error("Ошибка загрузки данных администратора");
                const adminJson = await adminRes.json();
                setAdminData(adminJson);

                const usersRes = await fetch(backendUrls.usersToActivate, {
                    credentials: 'include',
                });
                if (!usersRes.ok) throw new Error("Ошибка загрузки пользователей");
                const usersJson = await usersRes.json();
                setUsersToActivate(usersJson.users || []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const activateUser = async (userId) => {
        try {
            const response = await fetch(backendUrls.activateUser(userId), {
                method: "PATCH",
                credentials: "include",
            });
            if (!response.ok) throw new Error();
            setUsersToActivate(prev => prev.filter(user => user.id !== userId));
        } catch (err) {
            alert("Не удалось активировать пользователя");
        }
    };

    const handleLogout = async () => {
        try {
            await fetch(backendUrls.logout, {
                method: "POST",
                credentials: "include",
            });
            navigate("/login");
        } catch (err) {
            alert("Ошибка при выходе из системы");
        }
    };

    if (loading) return <div className="loading">Загрузка...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="account-page-container">
            <h2 className="account-title">Админ-панель</h2>

            <div className="buttons-grid">
                <button onClick={handleLogout} className="logout-button">
                    🚪 Выйти
                </button>
            </div>

            <div className="card">
                <h3>Информация о текущем пользователе</h3>
                <div className="info-grid">
                    <div className="info-item">
                        <span className="info-label">ФИО:</span>
                        <span className="info-value">
                            {adminData.last_name} {adminData.name} {adminData.patronymic}
                        </span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">Email:</span>
                        <span className="info-value">{adminData.email}</span>
                    </div>
                </div>
            </div>

            <div className="card">
                <h3>Пользователи на активацию</h3>
                {usersToActivate.length === 0 ? (
                    <p>Нет пользователей, ожидающих активации.</p>
                ) : (
                    <table className="users-table">
                        <thead>
                        <tr>
                            <th>ФИО</th>
                            <th>Email</th>
                            <th>Кафедра</th>
                            <th>Должность</th>
                            <th>Действие</th>
                        </tr>
                        </thead>
                        <tbody>
                        {usersToActivate.map(user => (
                            <tr key={user.id}>
                                <td>{user.last_name} {user.first_name} {user.patronymic}</td>
                                <td>{user.email}</td>
                                <td>{user.departament?.title || "—"}</td>
                                <td>{user.post}</td>
                                <td>
                                    <button
                                        className="small-activate-btn"
                                        onClick={() => activateUser(user.id)}
                                    >
                                        ✅ Активировать
                                    </button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}
