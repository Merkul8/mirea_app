import {backendUrls} from "../Utils/urls.js";
import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import '../Components/Metrcis/Dep/DepMetric.css';

export default function DepartamentMetricsPage() {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({
        publication_count: 0,
        authors_count: 0,
        k1_count: 0,
        k2_count: 0,
        k3_count: 0,
        rinc_count: 0,
        message: "",
    });
    const [departamentId, setDepartamentId] = useState(null); // Здесь будет твой id департамента
    const navigate = useNavigate();

    // Загружаем данные текущего пользователя
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch(backendUrls.me, {
                    credentials: "include",
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        navigate("/login");
                        return;
                    }
                    throw new Error("Ошибка загрузки данных пользователя");
                }

                const userData = await response.json();
                console.log(userData);
                setDepartamentId(userData.departament_id);
                setFormData(prev => ({
                    ...prev,
                    departament_id: userData.departament_id // Сохраняем departament_id в formData
                }));
            } catch (error) {
                console.error("Ошибка загрузки данных пользователя", error);
                navigate("/login");
            }
        };

        fetchUserData();
    }, [navigate]);

    // Загружаем метрики для текущего departamentId
    useEffect(() => {
        if (departamentId) {
            fetchMetrics(departamentId);
        }
    }, [departamentId]);

    const fetchMetrics = async (departamentId) => {
        try {
            const response = await fetch(backendUrls.departamentMetric(departamentId), {
                credentials: "include",
            });
            if (response.ok) {
                const data = await response.json();
                setMetrics(data);
            } else if (response.status === 404) {
                setMetrics(null);
            }
        } catch (error) {
            console.error("Ошибка загрузки метрик", error);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };

    const handleSave = async () => {
        try {
            const method = metrics ? "PUT" : "POST";
            const url = metrics ? backendUrls.updateDepMetric : backendUrls.createDepMetric;

            // здесь ЯВНО указываем departament_id
            const payload = {
                ...formData,
                departament_id: departamentId,  // <- 100% добавляем сюда
            };
            console.log("payload", payload)
            const response = await fetch(url, {
                method: method,
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                await fetchMetrics(departamentId);
                setShowModal(false);
            } else {
                alert("Ошибка сохранения метрик");
            }
        } catch (error) {
            console.error("Ошибка сохранения метрик", error);
        }
    };
    console.log(formData)

    const handleDelete = async () => {
        if (!metrics) return;
        if (!window.confirm("Вы уверены, что хотите удалить метрики?")) return;

        try {
            const url = backendUrls.deleteDepMetric + `?metric_id=${metrics.id}`;
            const response = await fetch(url, {
                method: "DELETE",
                credentials: "include",
            });

            if (response.ok) {
                setMetrics(null);
            } else {
                alert("Ошибка удаления метрик");
            }
        } catch (error) {
            console.error("Ошибка удаления метрик", error);
        }
    };

    if (loading) return <div className="loading">Загрузка...</div>;

    return (
        <>
            <div className="col-2 offset-4">
                <button
                    className="back-btn"
                    onClick={() => navigate(-1)}
                >
                    Назад
                </button>
            </div>
            <div className="departament-metrics-container">

                <h2>Управление метриками кафедры</h2>

                {metrics ? (
                    <>
                        <ul>
                            <li>Публикаций: {metrics.publication_count}</li>
                            <li>Авторов: {metrics.authors_count}</li>
                            <li>К1 публикаций: {metrics.k1_count}</li>
                            <li>К2 публикаций: {metrics.k2_count}</li>
                            <li>К3 публикаций: {metrics.k3_count}</li>
                            <li>РИНЦ публикаций: {metrics.rinc_count}</li>
                            {metrics.message && <li>Сообщение: {metrics.message}</li>}
                        </ul>
                        <button onClick={() => {
                            setFormData(metrics);
                            setShowModal(true);
                        }}>
                            Обновить метрику
                        </button>
                        <button className="danger-btn" onClick={handleDelete}>
                            Удалить метрику
                        </button>
                    </>
                ) : (
                    <>
                        <p>Метрика не найдена.</p>
                        <button onClick={() => {
                            setFormData({
                                publication_count: 0,
                                authors_count: 0,
                                k1_count: 0,
                                k2_count: 0,
                                k3_count: 0,
                                rinc_count: 0,
                                message: "",
                                departament_id: departamentId // Устанавливаем departament_id для создания новой метрики
                            });
                            setShowModal(true);
                        }}>
                            Добавить метрику
                        </button>
                    </>
                )}

                {showModal && (
                    <div className="modal-overlay">
                        <div className="modal-content">
                            <h3>{metrics ? "Обновить метрику" : "Создать метрику"}</h3>
                            <form>
                                <label>Публикаций:</label>
                                <input type="number" name="publication_count" value={formData.publication_count}
                                       onChange={handleChange}/>

                                <label>Авторов:</label>
                                <input type="number" name="authors_count" value={formData.authors_count}
                                       onChange={handleChange}/>

                                <label>К1 публикаций:</label>
                                <input type="number" name="k1_count" value={formData.k1_count} onChange={handleChange}/>

                                <label>К2 публикаций:</label>
                                <input type="number" name="k2_count" value={formData.k2_count} onChange={handleChange}/>

                                <label>К3 публикаций:</label>
                                <input type="number" name="k3_count" value={formData.k3_count} onChange={handleChange}/>

                                <label>РИНЦ публикаций:</label>
                                <input type="number" name="rinc_count" value={formData.rinc_count}
                                       onChange={handleChange}/>

                                <label>Сообщение:</label>
                                <textarea name="message" value={formData.message} onChange={handleChange}/>

                                <div className="modal-buttons">
                                    <button type="button" onClick={handleSave}>
                                        Сохранить
                                    </button>
                                    <button type="button" className="danger-btn" onClick={() => setShowModal(false)}>
                                        Отмена
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
