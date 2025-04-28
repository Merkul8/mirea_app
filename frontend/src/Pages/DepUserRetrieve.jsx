import {useParams, useLocation, useNavigate} from 'react-router-dom';
import {useEffect, useState} from "react";
import '../Components/DeparamentUsers/DepRetrieve/DepRetrieve.css';
import '../Components/DeparamentUsers/DepartamentsUsers.css'
import {backendUrls} from "../Utils/urls.js";

export default function DepUserRetrieve() {
    const {user_id} = useParams();
    const {state} = useLocation();
    const [user, setUser] = useState(state?.user || null);
    const [loading, setLoading] = useState(!state?.user);
    const [error, setError] = useState(null);

    const [depMetrics, setDepMetrics] = useState(null);
    const [userMetrics, setUserMetrics] = useState(null);

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState(null);

    const navigate = useNavigate();

    const [publications, setPublications] = useState([]);

    useEffect(() => {
        if (user) {
            fetch(backendUrls.get_publication_by_user_id(user.id),
                {
                    method: 'GET',
                    credentials: 'include',
                })
                .then(res => res.json())
                .then(data => setPublications(data.data || []));
        }
    }, [user, user_id]);

    useEffect(() => {
        if (user?.departament_id) {
            fetch(backendUrls.departamentMetric(user.departament_id), {
                method: 'GET',
                credentials: 'include',
            })
                .then(res => res.json())
                .then(data => setDepMetrics(data))
                .catch(err => console.error("Ошибка загрузки департамент метрик:", err));
        }
    }, [user]);

// Загружаем метрики пользователя
    useEffect(() => {
        if (user?.id) {
            fetch(backendUrls.userMetric(user.id), {
                method: 'GET',
                credentials: 'include',
            })
                .then(res => res.json())
                .then(data => setUserMetrics(data))
                .catch(err => console.error("Ошибка загрузки пользовательских метрик:", err));
        }
    }, [user]);

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка загрузки: {error.message}</div>;
    if (!user) return <div>Пользователь не найден</div>;

    return (
        <div className="user-detail-container">
            <button
                className="back-button"
                onClick={() => navigate(-1)}
            >
                ← Назад к списку
            </button>

            <div className="user-profile-card">
                <div className="user-header">
                    <h2>{user.last_name} {user.first_name} {user.patronymic}</h2>
                    <span className="user-id">ID: {user_id}</span>
                </div>

                <div className="user-info-section">
                    <h3>Основная информация</h3>
                    <div className="info-grid">
                        <div className="info-item">
                            <span className="info-label">Должность:</span>
                            <span className="info-value">{user.post}</span>
                        </div>
                        <div className="info-item">
                            <span className="info-label">Email:</span>
                            <span className="info-value">{user.email}</span>
                        </div>
                        <div className="info-item">
                            <span className="info-label">Тип работы:</span>
                            <span className="info-value">{user.work_type}</span>
                        </div>
                        {user.academic_degree && (
                            <div className="info-item">
                                <span className="info-label">Учёная степень:</span>
                                <span className="info-value">{user.academic_degree}</span>
                            </div>
                        )}
                    </div>
                </div>

                <div className="user-metrics">
                    <h3>Метрики</h3>

                    {depMetrics && !userMetrics ? (
                        <div className="metrics-block">
                            <h4>Метрики департамента</h4>
                            <ul>
                                <li>Публикаций: {depMetrics.publication_count}</li>
                                <li>Авторов: {depMetrics.authors_count}</li>
                                <li>К1 публикаций: {depMetrics.k1_count}</li>
                                <li>К2 публикаций: {depMetrics.k2_count}</li>
                                <li>К3 публикаций: {depMetrics.k3_count}</li>
                                <li>РИНЦ публикаций: {depMetrics.rinc_count}</li>
                                {depMetrics.message && <li>Сообщение: {depMetrics.message}</li>}
                            </ul>
                        </div>
                    ) : (
                        <p>Метрики кафедры отсутствуют или есть персональные метрики</p>
                    )}

                    {userMetrics ? (
                        <div className="metrics-block">
                            <h4>Персональные метрики</h4>
                            <ul>
                                <li>ID: {userMetrics.user_id}</li>
                                <li>Публикаций: {userMetrics.publication_count}</li>
                                <li>Авторов: {userMetrics.authors_count}</li>
                                <li>К1 публикаций: {userMetrics.k1_count}</li>
                                <li>К2 публикаций: {userMetrics.k2_count}</li>
                                <li>К3 публикаций: {userMetrics.k3_count}</li>
                                <li>РИНЦ публикаций: {userMetrics.rinc_count}</li>
                                {userMetrics.message && <li>Сообщение: {userMetrics.message}</li>}
                            </ul>
                            <button
                                className="edit-metrics-button"
                                onClick={() => {
                                    setFormData({...userMetrics}); // Копируем текущие данные в форму
                                    setIsModalOpen(true);
                                }}
                            >
                                ✏️ Редактировать метрики
                            </button>
                        </div>
                    ) : (
                        <p>Персональные метрики отсутствуют</p>
                    )}
                </div>

                <div className="user-publications">
                    <h3>Публикации</h3>
                    {publications.length > 0 ? (
                        <ul className="publications-list">
                            {publications.map((pub) => (
                                <li key={pub.id} className="publication-item">
                                    <h4>{pub.title}</h4>
                                    <p><strong>Год публикации:</strong> {pub.publication_year}</p>
                                    <p><strong>Авторы:</strong> {pub.authors}</p>
                                    <p><strong>Тип автора:</strong> {pub.author_type || "Не указан"}</p>
                                    <p><strong>Государственная служба:</strong> {pub.public_service ? "Да" : "Нет"}</p>
                                    <p><strong>Количество цитирований:</strong> {pub.citations}</p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>У пользователя нет публикаций</p>
                    )}
                </div>
                {isModalOpen && (
                    <div className="modal-overlay">
                        <div className="modal-content">
                            <h3>Редактирование метрик</h3>
                            <form
                                onSubmit={(e) => {
                                    e.preventDefault();
                                    fetch(backendUrls.update_user_metrics, {
                                        method: 'PUT',
                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                        credentials: 'include',
                                        body: JSON.stringify(formData),
                                    })
                                        .then(res => {
                                            if (!res.ok) throw new Error('Ошибка обновления метрик');
                                            return res.json();
                                        })
                                        .then(() => {
                                            setUserMetrics(formData);
                                            setIsModalOpen(false);
                                        })
                                        .catch(err => alert(err.message));
                                }}
                            >
                                <label>Публикаций:
                                    <input
                                        type="number"
                                        value={formData.publication_count}
                                        onChange={(e) => setFormData({
                                            ...formData,
                                            publication_count: Number(e.target.value)
                                        })}
                                    />
                                </label>
                                <label>Авторов:
                                    <input
                                        type="number"
                                        value={formData.authors_count}
                                        onChange={(e) => setFormData({
                                            ...formData,
                                            authors_count: Number(e.target.value)
                                        })}
                                    />
                                </label>
                                <label>К1 публикаций:
                                    <input
                                        type="number"
                                        value={formData.k1_count}
                                        onChange={(e) => setFormData({...formData, k1_count: Number(e.target.value)})}
                                    />
                                </label>
                                <label>К2 публикаций:
                                    <input
                                        type="number"
                                        value={formData.k2_count}
                                        onChange={(e) => setFormData({...formData, k2_count: Number(e.target.value)})}
                                    />
                                </label>
                                <label>К3 публикаций:
                                    <input
                                        type="number"
                                        value={formData.k3_count}
                                        onChange={(e) => setFormData({...formData, k3_count: Number(e.target.value)})}
                                    />
                                </label>
                                <label>РИНЦ публикаций:
                                    <input
                                        type="number"
                                        value={formData.rinc_count}
                                        onChange={(e) => setFormData({...formData, rinc_count: Number(e.target.value)})}
                                    />
                                </label>
                                <label>Сообщение:
                                    <input
                                        type="text"
                                        value={formData.message || ''}
                                        onChange={(e) => setFormData({...formData, message: e.target.value})}
                                    />
                                </label>

                                <div className="modal-buttons">
                                    <button type="submit">Сохранить</button>
                                    <button type="button" onClick={() => setIsModalOpen(false)}>Отмена</button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

            </div>
        </div>

    )

}