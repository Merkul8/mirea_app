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
                {/* Дополнительные секции можно добавить здесь */}
            </div>
        </div>
    )

}