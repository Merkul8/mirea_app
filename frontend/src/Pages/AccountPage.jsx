import {backendUrls} from "../Utils/urls.js";
import {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import '../Components/Auth/Account/Account.css';


export default function AccountPage() {

    const [userData, setUserData] = useState(null);
    const [publications, setPublications] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [pubLoading, setPubLoading] = useState(true);
    const [pubError, setPubError] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch(backendUrls.me, {
                    credentials: 'include', // Для отправки кук
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        navigate('/login');
                        return;
                    }
                    throw new Error('Ошибка загрузки данных');
                }

                const data = await response.json();
                console.log(data)
                setUserData(data);

                const pubResponse = await fetch(backendUrls.userPublications, {
                    credentials: 'include',
                });

                if (!pubResponse.ok) {
                    throw new Error('Ошибка загрузки публикаций');
                }

                const pubData = await pubResponse.json();
                setPublications(pubData.data || []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
                setPubLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

    if (loading) {
        return <div className="loading">Загрузка профиля...</div>;
    }

    if (error) {
        return <div className="error">Ошибка: {error}</div>;
    }
    console.log(userData)
    const isBoss = userData.roles && userData.roles.includes('boss')

    return (
        <div className="profile-container">
            <h2>Мой профиль</h2>

            <div className="profile-section">
                <h3>Основная информация</h3>
                <div className="profile-field">
                    <span className="field-label">ФИО:</span>
                    <span className="field-value">
            {userData.last_name} {userData.name} {userData.patronymic}
          </span>
                </div>
                <div className="profile-field">
                    <span className="field-label">Email:</span>
                    <span className="field-value">{userData.email}</span>
                </div>
            </div>

            <div className="profile-section">
                <h3>Профессиональная информация</h3>
                <div className="profile-field">
                    <span className="field-label">Должность:</span>
                    <span className="field-value">{userData.post}</span>
                </div>
                <div className="profile-field">
                    <span className="field-label">Тип работы:</span>
                    <span className="field-value">{userData.work_type}</span>
                </div>
                <div className="profile-field">
                    <span className="field-label">Учёная степень:</span>
                    <span className="field-value">{userData.academic_degree}</span>
                </div>
                <div className="profile-field">
                    <span className="field-label">ELIBRARY ID:</span>
                    <span className="field-value">{userData.elibrary_id}</span>
                </div>
            </div>

            <button
                className="edit-btn"
                onClick={() => navigate('/profile/edit')}
            >
                Редактировать профиль
            </button>

            {isBoss && (
                <button
                    className="boss-btn"
                    onClick={() => navigate('/users/departament')}
                >
                    Управление отделом
                </button>
            )}

            <div className="profile-section">
                <h3>Публикации</h3>
                {pubLoading ? (
                    <div className="loading">Загрузка публикаций...</div>
                ) : pubError ? (
                    <div className="error">Ошибка загрузки публикаций: {pubError}</div>
                ) : publications.length === 0 ? (
                    <p>У вас пока нет публикаций</p>
                ) : (
                    <div className="publications-list">
                        {publications.map((pub) => (
                            <div key={pub.id} className="publication-item">
                                <h4>{pub.title}</h4>
                                <p><strong>Авторы:</strong> {pub.authors}</p>
                                <p><strong>Год:</strong> {pub.publication_year}</p>
                                <p><strong>Цитирования:</strong> {pub.citations || 'нет данных'}</p>
                                <p><strong>Тип автора:</strong> {pub.author_type}</p>
                                {pub.public_service && (
                                    <p><strong>Сервис:</strong> {pub.public_service}</p>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <button
                className="edit-btn"
                onClick={() => navigate('/profile/edit')}
            >
                Редактировать профиль
            </button>
        </div>
    );
}