<template>
  <div>
    <h3>Логи работы</h3>
    <textarea v-model="logs" rows="10" cols="50" readonly></textarea>
  </div>
</template>

<script>
export default {
  data() {
    return {
      logs: "Логи работы нейросети появятся здесь...",
    };
  },
};
</script>