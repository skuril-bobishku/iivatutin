<template>
  <div class="home">
    <h1>Обучение и распознавание изображений</h1>
    <FileUploader />
    <ModelSelector />
    <ChartDisplay />
    <LogOutput />
  </div>
</template>

<script>
import FileUploader from "../components/FileUploader.vue";
import ModelSelector from "../components/ModelSelector.vue";
import ChartDisplay from "../components/ChartDisplay.vue";
import LogOutput from "../components/LogOutput.vue";

export default {
  name: "HomeView",
  components: {
    FileUploader,
    ModelSelector,
    ChartDisplay,
    LogOutput,
  },
};
</script>