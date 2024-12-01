<template>
  <div>
    <h3>Загрузка данных для обучения или распознавания</h3>
    <input type="file" multiple @change="handleFiles" />
  </div>
</template>

<script>
export default {
  methods: {
    handleFiles(event) {
      const files = event.target.files;
      console.log("Выбранные файлы:", files);
      // Загрузите файлы на сервер или обработайте локально
    },
  },
};
</script>