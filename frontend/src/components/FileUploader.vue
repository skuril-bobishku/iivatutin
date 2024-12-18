<template>
  <div class="content-view file-uploader">
    <h3>Загрузка .zip для обучения или распознавания</h3>
    <input type="file" multiple @change="handleFiles" />
    <button @click="uploadFile" >Загрузка</button>
  </div>
</template>

<script>
import '../assets/file-uploader/file-uploader.css'
import { EventBus } from "@/eventBus.js";

export default {
  data() {
    return {
      serverUrl: import.meta.env.VITE_SERVER_DOMAIN,
      serverPort: import.meta.env.VITE_SERVER_PORT,
      file: null,
      filePath: "",
    };
  },
  methods: {
    handleFiles(event) {
      this.file = event.target.files[0];
    },
    async uploadFile(){
      if (!this.file) {
        alert("Добавьте файл .zip");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.file);

      try {
        const response = await fetch(`http://${this.serverUrl}:${this.serverPort}/upload`, {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          throw new Error("Upload failed");
        }

        if (response.status === 201) {
          const data = await response.json();
          this.filePath = data.path;
          EventBus.sFilePath(this.filePath);
          alert("File uploaded successfully!");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Error uploading file");
      }
    }
  },
};
</script>