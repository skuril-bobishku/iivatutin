<template>
  <div class="file-uploader">
    <h3>Загрузка .zip для обучения или распознавания</h3>
    <input type="file" multiple @change="handleFiles" />
  </div>
</template>

<script>
import '../assets/file-uploader/file-uploader.css'

export default {
  methods: {
    handleFiles(event) {
      const files = event.target.files;
      console.log("Выбранные файлы:", files);
    },
  },
};
</script>