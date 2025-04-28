import {backendUrls} from "../../Utils/urls.js";
import {useEffect, useState} from "react";
import {useNavigate, Link} from "react-router-dom";
import './DepartamentsUsers.css'


export default function DepartamentUsers() {
    const [usersData, setUsersData] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {

                const usersDep = await fetch(backendUrls.usersDepartament, {
                    credentials: 'include',
                });

                if (!usersDep.ok) {
                    throw new Error('Ошибка загрузки публикаций');
                }

                const usersDepData = await usersDep.json();
                setUsersData(usersDepData.data || []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

    if (loading) {
        return <div className="loading">Загрузка данных...</div>;
    }

    if (error) {
        return <div className="error">Ошибка: {error}</div>;
    }

    return (
        <div className="department-users-container">
            <h2>Пользователи отдела</h2>

            <button
                className="back-btn"
                onClick={() => navigate(-1)}
            >
                Назад
            </button>

            {usersData.length === 0 ? (
                <p>В вашем отделе нет других пользователей</p>
            ) : (
                <div className="users-list">
                    {usersData.map((user, index) => (
                        <div className="container">
                            <div className="row">
                                <Link to={`/users/departament/${user.id}`} state={{user}}>
                                    <div key={index} className="user-card">
                                        <h3>{user.last_name} {user.first_name} {user.patronymic}</h3>
                                        <div className="user-info">
                                            <p><strong>Должность:</strong> {user.post}</p>
                                            <p><strong>Email:</strong> {user.email}</p>
                                            <p><strong>Тип работы:</strong> {user.work_type}</p>
                                            {user.academic_degree && (
                                                <p><strong>Учёная степень:</strong> {user.academic_degree}</p>
                                            )}
                                        </div>
                                    </div>
                                </Link>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}