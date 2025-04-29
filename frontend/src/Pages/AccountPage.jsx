import {backendUrls} from "../Utils/urls.js";
import {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import Modal from 'react-modal';
import '../Components/Auth/Account/Account.css';

export default function AccountPage() {

    const [userData, setUserData] = useState(null);
    const [publications, setPublications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pubLoading, setPubLoading] = useState(true);
    const [pubError, setPubError] = useState(null);

    const [editingPublication, setEditingPublication] = useState(null);
    const [editFormData, setEditFormData] = useState({
        id: '',
        citations: '',
        title: '',
        public_service: '',
        authors: '',
        publication_year: '',
        author_type: '',
    });

    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch(backendUrls.me, {
                    credentials: 'include',
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        navigate('/login');
                        return;
                    }
                    throw new Error('Ошибка загрузки данных');
                }

                const data = await response.json();
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
                navigate("/login");
            } finally {
                setLoading(false);
                setPubLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

    const openEditModal = (pub) => {
        setEditFormData(pub);
        setEditingPublication(pub);
    };

    const closeEditModal = () => {
        setEditingPublication(null);
    };

    const handleEditChange = (e) => {
        const {name, value} = e.target;
        setEditFormData(prev => ({...prev, [name]: value}));
    };

    const handleEditSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(backendUrls.updatePublication, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(editFormData),
            });

            if (!response.ok) {
                throw new Error('Ошибка при обновлении публикации');
            }

            setPublications(prev =>
                prev.map(pub => (pub.id === editFormData.id ? editFormData : pub))
            );

            closeEditModal();
        } catch (err) {
            console.error(err);
            alert('Не удалось обновить публикацию.');
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

    if (loading) {
        return <div className="loading">Загрузка профиля...</div>;
    }

    if (error) {
        return <div className="error">Ошибка: {error}</div>;
    }

    const isBoss = userData.roles && userData.roles.includes('boss');

    return (
        <div className="account-page-container">
            <div className="header-with-buttons">
                <h2 className="account-title">Мой профиль</h2>
                <div className="buttons-grid">
                    <button className="edit-btn" onClick={() => navigate('/profile/edit')}>
                        Редактировать профиль
                    </button>
                    <button onClick={handleLogout} className="logout-button">
                        🚪 Выйти
                    </button>
                    {isBoss && (
                        <>
                            <button className="boss-btn" onClick={() => navigate('/users/departament')}>
                                Управление отделом
                            </button>
                            <button className="boss-btn" onClick={() => navigate('/departament/metrics')}>
                                Руководство метриками кафедры
                            </button>
                        </>
                    )}
                </div>
            </div>

            <div className="card">
                <h3>Основная информация</h3>
                <div className="info-grid">
                    <div className="info-item">
                        <span className="info-label">ФИО:</span>
                        <span className="info-value">{userData.last_name} {userData.name} {userData.patronymic}</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">Email:</span>
                        <span className="info-value">{userData.email}</span>
                    </div>
                </div>
            </div>

            <div className="card">
                <h3>Профессиональная информация</h3>
                <div className="info-grid">
                    <div className="info-item">
                        <span className="info-label">Должность:</span>
                        <span className="info-value">{userData.post}</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">Тип работы:</span>
                        <span className="info-value">{userData.work_type}</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">Учёная степень:</span>
                        <span className="info-value">{userData.academic_degree}</span>
                    </div>
                    <div className="info-item">
                        <span className="info-label">ELIBRARY ID:</span>
                        <span className="info-value">{userData.elibrary_id}</span>
                    </div>
                </div>
            </div>

            <div className="card">
                <h3>Публикации</h3>
                {pubLoading ? (
                    <div className="loading">Загрузка публикаций...</div>
                ) : pubError ? (
                    <div className="error">Ошибка загрузки публикаций: {pubError}</div>
                ) : publications.length === 0 ? (
                    <p>У вас пока нет публикаций</p>
                ) : (
                    <div className="publications-grid">
                        {publications.map((pub) => (
                            <div key={pub.id} className="publication-card">
                                <div className="publication-header">
                                    <h4>{pub.title}</h4>
                                    <button className="small-edit-btn" onClick={() => openEditModal(pub)}>✏️</button>
                                </div>
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

            {/* Модалка редактирования публикации */}
            <Modal
                isOpen={!!editingPublication}
                onRequestClose={closeEditModal}
                contentLabel="Редактировать публикацию"
                className="edit-modal"
                overlayClassName="edit-modal-overlay"
            >
                <h2>Редактировать публикацию</h2>
                <form onSubmit={handleEditSubmit} className="edit-form">
                    {Object.keys(editFormData).map((key) => (
                        key !== "id" ? (
                            <div key={key} className="form-group">
                                <label>{key}</label>
                                <input
                                    type="text"
                                    name={key}
                                    value={editFormData[key] || ''}
                                    onChange={handleEditChange}
                                />
                            </div>
                        ) : null
                    ))}
                    <button type="submit" className="save-btn">Сохранить</button>
                </form>
            </Modal>
        </div>
    );
}
