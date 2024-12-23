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
    startAugmentation() {

    },
    startTrain () {

    }
  },
};
</script>