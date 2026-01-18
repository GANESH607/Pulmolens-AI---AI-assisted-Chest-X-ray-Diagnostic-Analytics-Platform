import axios from "axios";

export const predictImage = async (formData) => {
  return await axios.post("http://127.0.0.1:5000/predict", formData);
};
