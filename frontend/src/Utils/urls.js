const baseBackend = 'http://localhost:5000';

const buildUrl = (baseUrl, url) => baseUrl + url

export const backendUrls = {
  base: baseBackend,
  register: buildUrl(baseBackend, "/register/"),
  login: buildUrl(baseBackend, "/login/"),
  varify: buildUrl(baseBackend, "/activate_account/"),
  me: buildUrl(baseBackend, "/me/"),
  userPublications: buildUrl(baseBackend, "/user/publications/"),
  usersDepartament: buildUrl(baseBackend, "/department-users/"),
  get_publication_by_user_id: (user_id) => buildUrl(baseBackend, `/user/publications/read/${user_id}/`),
  userMetric: (user_id) => buildUrl(baseBackend, `/metrics/${user_id}/`),
  departamentMetric: (departament_id) => buildUrl(baseBackend, `/metrics/departament/${departament_id}/`),
}