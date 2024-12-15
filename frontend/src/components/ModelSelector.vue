<template>
  <div>
    <h3>Выбор модели</h3>
    <button @click="selectModel">Выбрать обученную модель</button>
    <button @click="retrainModel">Переобучить модель</button>
  </div>
</template>

<script>
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