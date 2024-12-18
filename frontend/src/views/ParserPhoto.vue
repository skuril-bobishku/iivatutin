<template>
    <div class="content-view">
      <div class="parser-list">
        <ul class="content-table">
          <li v-for="(item, index) in items" :key="index">
            <span class="text-url">{{ item }}</span>
            <button
                @click="remItem(index)">–</button><!--v-show="currentStage === 'parser'"-->
            <span class="indicator"></span>
          </li>
        </ul>
      </div>
      <div class="parser-input">
        <input
            type="text"
            class="input-text"
            placeholder="Введите URL адрес"
            v-model="inputURL"
            @keydown.enter="addItem"
        />
        <button
            class="input-button"
            @click="addItem"
        >+</button>
      </div>
      <div class="parser-config">
        <input
            type="text"
            class="input-text"
            placeholder="Введите отступ"
            v-model="inputOffset"
            @keydown.enter="startParsing"
        />
        <input
            type="text"
            class="input-text"
            placeholder="Введите количество"
            v-model="inputCount"
            @keydown.enter="startParsing"
        />
      </div>
      <div class="parser-buttons">
        <button class="input-button start"
                @click="startParsing"
        >Парсинг</button>
        <button class="input-button next"
                v-show="isFilesUploaded"
                @click="nextPage"
        >
          <svg xmlns="http://www.w3.org/2000/svg"
               width="24"
               height="24"
               viewBox="0 0 24 20">
            <path fill="none"
                  stroke="#ffffff"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="m21 12l-5-5m5 5l-5 5m5-5H3"></path>
          </svg>
        </button>
      </div>
    </div>
</template>

<script>
import { getUrl, getPort } from '@/env.js';
import '@/assets/parser/parser-list.css';
import '@/assets/parser/parser-input.css';
import '@/assets/parser/parser-config.css';
import '@/assets/parser/parser-buttons.css';

export default {
  name: "ParserView",
  data() {
    return {
      inputURL: "",
      items: [],
      inputOffset: "",
      inputCount: "",
      isFilesUploaded: false,
      folderName: "",
    };
  },
  methods: {
    addItem() {
      if (this.inputURL.trim() !== "") {
        this.items.push(this.inputURL.trim());
        this.inputURL = "";
      }
    },
    remItem(index) {
      this.items.splice(index, 1);
    },
    async startParsing() {
      const count = this.inputCount.trim();
      const offset = this.inputOffset.trim();

      if (!count || !offset) {
        alert("Пожалуйста, заполните оба поля: количество и отступ!");
        return;
      }

      if (!this.isValidNumber(count)) {
        alert("Введите корректное количество (целое число)!");
        return;
      }

      if (!this.isValidNumber(offset)) {
        alert("Введите корректный отступ (целое число)!");
        return;
      }

      if (this.items.length === 0) {
        alert("Отсутствуют URL в списке!");
        return;
      }

      try {
        const requests = this.items.map(url => {
          const serverUrl = getUrl('VITE_API_SERVER_URL');
          const serverPort = getPort('VITE_API_SERVER_PORT');
          const encodedURL = encodeURIComponent(url);

          return fetch(`http://${serverUrl}:${serverPort}/parse?url=${encodedURL}&count=${count}&skip=${offset}`)
            .then(response => {
              if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              return response.json();
            })
            .then(data => {
              if (data && data.path) {
                this.folderName = data.path;
                alert(`Сохранено в ${this.folderName}`);
                this.isFilesUploaded = true;
              } else {
                throw new Error("No 'path' field in the response.");
              }
            })
            .then(this.nextPage);
        });

        const results = await Promise.all(requests);
        console.log("Results from all URLs:", results);

        const allItems = results.flatMap(result => result.items || []);
        this.items = allItems;

      } catch (error) {
        console.error("Error parsing data:", error);
      }
    },
    nextPage() {
      //this.$router.push({ name: "Home" });
      this.$emit('nextPage', this.folderName);
    },
    isValidNumber(value) {
      return !isNaN(value) && Number.isInteger(Number(value)) && Number(value) >= 0;
    },
  },
}
</script>