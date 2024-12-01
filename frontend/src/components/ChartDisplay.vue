<template>
  <div>
    <h3>График производительности нейросети</h3>
    <canvas id="chart"></canvas>
  </div>
</template>

<script>
import { onMounted } from "vue";
import { Chart } from "chart.js";

export default {
  name: "ChartDisplay",
  setup() {
    onMounted(() => {
      const ctx = document.getElementById("chart").getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: ["Эпоха 1", "Эпоха 2", "Эпоха 3"],
          datasets: [
            {
              label: "Точность",
              data: [0.8, 0.85, 0.9],
              borderColor: "blue",
              fill: false,
            },
          ],
        },
      });
    });
  },
};
</script>