import axios from "axios";

export function authenticateUser(username, password) {
  const data = {
    username: username,
    password: password,
  };

  return axios
    .post("http://localhost:5000/login", data)
    .then((response) => {
      // Traitez la réponse de l'API ici, par exemple, stockez le token d'authentification dans le local storage
      console.log("success");
      return response.data;
    })
    .catch((error) => {
      // Traitez l'erreur ici, par exemple, affichez un message d'erreur à l'utilisateur
      console.log("error");
      console.error(error);
    });
}
export function registerUser(username, password) {
  const userData = {
    username: username,
    password: password,
  };

  return axios.post("http://localhost:5000/utilisateurs", userData);
}
