<template>
  <div class="model-selector">
    <h3>Обучение модели</h3>
    <div class="parse-input">
      <input
          type="text"
          placeholder="Введите количество эпох"
          v-model="inputURL"
          @keydown.enter="addItem"
      />
    </div>
    <button @click="selectModel">Выбрать обученную модель</button>
    <button @click="retrainModel">Переобучить модель</button>
  </div>
</template>

<script>
import '../assets/model-selector/model-selector.css'
import { EventBus } from "@/eventBus.js";

export default {
  computed: {
    gFilePath() {
      return EventBus.sFilePath;
    },
    gProjName() {
      return EventBus.sProjName;
    }
  },
  methods: {
    selectModel() {
      console.log("Выбор обученной модели");
    },
    retrainModel() {
      console.log("Переобучение модели");
    },
  },
};
</script>