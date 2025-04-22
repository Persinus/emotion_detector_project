<template>
  <div>
    <h1>Emotion Detection</h1>

    <!-- Display the image before or after selecting -->
    <div class="image-preview">
      <img :src="imagePreview" alt="Image Preview" v-if="imagePreview" />
      <p v-if="!selectedImage" class="no-image">No image selected yet</p>
    </div>

    <!-- Select file -->
    <input type="file" @change="onFileChange" />

    <!-- Prediction button -->
    <button @click="makePrediction">Predict Emotion</button>

    <!-- Display prediction or error -->
    <p v-if="prediction" class="prediction-result">Prediction: {{ prediction }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- Display image with face highlighted -->
    <div v-if="imageWithFaces">
      <img :src="imageWithFaces" alt="Image with Faces" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      prediction: null,
      selectedImage: null,
      imagePreview: null,  // Holds the image preview URL
      imageWithFaces: null, // Holds the image with faces highlighted
      errorMessage: null,  // Holds the error message if any
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];  // Get the selected file
      if (file) {
        this.selectedImage = file;
        this.imagePreview = URL.createObjectURL(file);  // Create preview URL for the selected image
        this.errorMessage = null;  // Clear any previous error message
      }
    },
    async makePrediction() {
      try {
        if (!this.selectedImage) {
          this.errorMessage = "Please select an image first!";
          return;
        }

        // Create FormData to send the image
        const formData = new FormData();
        formData.append('file', this.selectedImage);

        // Send the image to the Flask server
        const response = await axios.post('http://127.0.0.1:5000/predict', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'  // Ensure the content type is 'multipart/form-data'
          }
        });

        this.prediction = response.data.prediction;
        this.errorMessage = null;  // Clear error message if prediction is successful
        this.imageWithFaces = `data:image/png;base64,${btoa(String.fromCharCode(...new Uint8Array(response.data.image)))}`;
      } catch (error) {
        this.errorMessage = "Error making prediction: " + error.message;
        this.prediction = null;  // Clear prediction if error occurs
        this.imageWithFaces = null; // Clear the image if error occurs
      }
    }
  }
}
</script>

<style scoped>
/* Your CSS styles */
.image-preview {
  text-align: center;
  margin-bottom: 20px;
}

.no-image {
  color: red;
  font-size: 18px;
}

.prediction-result {
  color: green;
}

.error-message {
  color: red;
}

img {
  width: 100%;
  max-width: 400px;
  display: block;
  margin: 20px auto;
}
</style>