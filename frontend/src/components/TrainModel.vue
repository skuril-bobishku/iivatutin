<template>
  <div class="content-view train-model">
    <h3>Обучение модели</h3>
    <div class="selector-buttons">
      <input type="checkbox" v-model="doAugmentation" />
      <label>Аугментация {{ doAugmentation ? 'включёна' : 'выключена' }}</label>
      <button v-show="doAugmentation"
              class="input-button start"
              @click="startAugmentation"
      >Аугментировать</button>
    </div>
    <button class="input-button start"
            @click="startTrain"
    >Обучить</button>
  </div>
</template>

<script>
import {getPort, getUrl} from "@/env.js";

export default {
  name: "TrainModel",
  props: {
    pName: {
      type: String,
      required: true,
    },
    mName: {
      type: String,
      required: true,
    },
    fPath: {
      type: String,
      required: true,
    },
    mEpochs: {
      type: Number,
      required: true,
    },
    mBatch: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      projectName: this.pName,
      modelName: this.mName,
      filePath: this.fPath,
      epochs: this.mEpochs,
      batch: this.mBatch,
      doAugmentation: false,
    };
  },
  watch: {
    pName(prName) {
      this.projectName = prName;
    },
    mName(moName) {
      this.modelName = moName;
    },
    fPath(newPath) {
      this.filePath = newPath;
    },
    mEpochs(ep) {
      this.epochs = ep;
    },
    mBatch(ba) {
      this.batch = ba;
    },
  },
  methods: {
    async startAugmentation() {
      try {
        const yoloUrl = getUrl('VITE_API_YOLO_URL');
        const yoloPort = getPort('VITE_API_YOLO_PORT');

        const response = await fetch(`http://${yoloUrl}:${yoloPort}/augment`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            fPath: this.filePath,
          }),
        });

        if (!response.ok) {
          throw new Error(`Ошибка: ${response.status}`);
        }

        const data = await response.json();
        alert("Аугментация завершена: " + JSON.stringify(data));
      } catch (error) {
        console.error("Ошибка при аугментации:", error);
        alert("Ошибка при аугментации: " + error.message);
      }
    },
    async startTrain () {
      try {
        const yoloUrl = getUrl('VITE_API_YOLO_URL');
        const yoloPort = getPort('VITE_API_YOLO_PORT');

        const response = await fetch(`http://${yoloUrl}:${yoloPort}/train`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            pName: this.projectName,
            //mName: this.modelName,
            fPath: this.filePath,
            epochs: this.epochs,
            batch: this.batch,
          }),
        });

        if (!response.ok) {
          throw new Error(`Ошибка: ${response.status}`);
        }

        const data = await response.json();
        alert("Обучение завершено: " + JSON.stringify(data));
      } catch (error) {
        console.error("Ошибка при обучении:", error);
        alert("Ошибка при обучении: " + error.message);
      }
    },
  },
};
</script>