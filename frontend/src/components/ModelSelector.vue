<template>
  <div class="content-view model-selector">
    <h3>Выбор модели</h3>
    <div class="selector-buttons">
      <button
          class="input-button"
          @click="selectModel"
      >Выбрать обученную модель</button>
      <button
          class="input-button"
          @click="retrainModel"
      >Обучить новую модель</button>
    </div>
  </div>
</template>

<script>
import '@/assets/model-selector/model-selector.css'

export default {
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