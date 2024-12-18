<template>
  <div class="content-view file-uploader">
    <h3>Загрузка .zip для обучения или распознавания</h3>
    <input type="file" multiple @change="handleFiles" />
    <button class="input-button"
        @click="uploadFile" >Загрузка</button>
  </div>
</template>

<script>
import {getPort, getUrl} from "@/env.js";
import '../assets/file-uploader/file-uploader.css'

export default {
  name: "FileUploader",
  props: {
    pName: {
      type: String,
      required: true,
    },
    fPath: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      projectName: this.pName,
      filePath: this.fPath,
      file: null,
    };
  },
  watch: {
    pName(newName) {
      this.projectName = newName;
    },
    fPath(newPath) {
      this.filePath = newPath;
    },
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
        const serverUrl = getUrl('VITE_API_SERVER_URL');
        const serverPort = getPort('VITE_API_SERVER_PORT');

        const response = await fetch(`http://${serverUrl}:${serverPort}/upload`, {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          throw new Error("Ошибка загрузки");
        }

        if (response.status === 201) {
          const data = await response.json();
          this.filePath = data.path;
          alert("Успешная загрузка");
          this.nextPage();
        }
      } catch (error) {
        alert(`Ошибка загрузки: ${error}`);
      }
    },
    nextPage() {
      this.$emit('nextPageTrain', this.projectName, this.filePath);
    },
  },
};
</script>