<template>
  <div class="content-view model-selector">
    <h3>Выбор модели YOLO</h3>
    <div class="selector-buttons">
      <button
          class="input-button"
          @click="selectModel"
      >Предобученная модель</button>
      <button
          class="input-button"
          @click="trainModel"
      >Обучить новую модель</button>
    </div>
    <div class="extended-content">
      <input class="input-file"
             type="file"
             v-show="!doNew"
             @change="handleFile" />
      <div class="trainer-content"
           v-show="doNew">
        <div class="row-content">
          <h3>Epochs</h3>
          <input type="text"
                 class="input-text"
                 placeholder="epochs"
                 v-model="epochs"
          />
        </div>
        <div class="row-content">
          <h3>Batch</h3>
          <input type="text"
                 class="input-text"
                 placeholder="batch"
                 v-model="batch"
          />
        </div>
      </div>
      <button class="input-button"
              @click="!doNew ? uploadFile() : makeModel()"
              :disabled="!doNew ? !isLoaded : !epochs || !batch"
      >{{ doNew ? 'Обучить' : 'Загрузить'}}</button>
    </div>
  </div>
</template>

<script>
import '@/assets/model-selector/model-selector.css'
import {getPort, getUrl} from "@/env.js";

export default {
  name: "ModelSelector",
  props: {
    pName: {
      type: String,
      required: true,
    },
    mName: {
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
      epochs: this.mEpochs,
      batch: this.mBatch,
      isLoaded: false,
      doNew: false,
    };
  },
  watch: {
    pName(prName) {
      this.projectName = prName;
    },
    mName(moName) {
      this.modelName = moName;
    },
    mEpochs(ep) {
      this.epochs = parseInt(ep, 10);
    },
    mBatch(ba) {
      this.batch = parseInt(ba, 10);
    },
  },
  methods: {
    selectModel() {
      this.doNew = false;
    },
    trainModel() {
      this.doNew = true;
    },
    handleFile(event) {
      this.file = event.target.files[0];
      this.file ? this.isLoaded = true : this.isLoaded = false;
    },
    makeModel() {
      this.modelNext();
    },
    async uploadFile(){
      if (!this.file) {
        alert("Добавьте файл .pt");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.file);

      try {
        const serverUrl = getUrl('VITE_API_SERVER_URL');
        const serverPort = getPort('VITE_API_SERVER_PORT');

        const response = await fetch(`http://${serverUrl}:${serverPort}/model?name=${this.projectName}`, {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          throw new Error("Ошибка загрузки");
        }

        if (response.status === 201) {
          const data = await response.json();
          this.modelName = data.path;

          alert("Успешная загрузка");
          this.modelNext();
        }
      } catch (error) {
        alert(`Ошибка загрузки: ${error}`);
      }
    },
    modelNext() {
      if (this.doNew) {
        this.$emit('modelNext', this.projectName, this.modelName, '', this.epochs, this.batch);
      }
      else {
        this.$emit('modelNext', this.projectName, this.modelName, '', -1, -1);
      }
    },
  },
};
</script>