const baseBackend = 'http://localhost:5000';

const buildUrl = (baseUrl, url) => baseUrl + url

export const backendUrls = {
  base: baseBackend,
  register: buildUrl(baseBackend, "/register/"),
  login: buildUrl(baseBackend, "/login/"),
  logout: buildUrl(baseBackend, "/logout/"),
  varify: buildUrl(baseBackend, "/activate_account/"),
  me: buildUrl(baseBackend, "/me/"),
  userPublications: buildUrl(baseBackend, "/user/publications/"),
  usersDepartament: buildUrl(baseBackend, "/department-users/"),
  get_publication_by_user_id: (user_id) => buildUrl(baseBackend, `/user/publications/read/${user_id}/`),
  userMetric: (user_id) => buildUrl(baseBackend, `/metrics/${user_id}/`),
  update_user_metrics:  buildUrl(baseBackend, "/metrics/update"),
  createUserMetric:  buildUrl(baseBackend, "/metrics/create"),
  deleteUserMetric:  buildUrl(baseBackend, "/metrics/delete"),
  departamentMetric: (departament_id) => buildUrl(baseBackend, `/metrics/departament/${departament_id}/`),
  deleteDepMetric:  buildUrl(baseBackend, "/metrics/departament/delete"),
  createDepMetric:  buildUrl(baseBackend, "/metrics/departament/create"),
  updateDepMetric:  buildUrl(baseBackend, "/metrics/departament/update"),
  updateUser:  buildUrl(baseBackend, "/users/update"),
  updatePublication:  buildUrl(baseBackend, "/user/publications/update"),
  usersToActivate:  buildUrl(baseBackend, "/users_to_activate/"),
  activateUser: (userId) => buildUrl(baseBackend, `/activate_user/${userId}`),
}