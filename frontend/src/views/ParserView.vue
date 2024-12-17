<template>
    <div class="parser">
      <div class="parse-list">
        <ul>
          <li v-for="(item, index) in items" :key="index">
            <span class="text-url">{{ item }}</span>
            <button @click="remItem(index)">–</button>
          </li>
        </ul>
      </div>
      <div class="parse-input">
        <input
            type="text"
            placeholder="Введите URL адрес"
            v-model="inputURL"
            @keydown.enter="addItem"
        />
        <button @click="addItem">+</button>
      </div>
      <div class="parse-config">
        <input
            type="text"
            placeholder="Введите отступ"
            v-model="inputOffset"
            @keydown.enter="startParsing"
        />
        <input
            type="text"
            placeholder="Введите количество"
            v-model="inputCount"
            @keydown.enter="startParsing"
        />
      </div>
      <div class="parse-buttons">
        <button class="start" @click="startParsing">Парсинг</button>
        <button class="next" :disabled="isFileUploaded" @click="nextPage">
          <svg xmlns="http://www.w3.org/2000/svg"
               width="32"
               height="32"
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
import '@/assets/parser/parser.css';
import '@/assets/parser/parse-list.css';
import '@/assets/parser/parse-input.css';
import '@/assets/parser/parse-config.css';
import '@/assets/parser/parse-buttons.css';

export default {
  name: "ParserView",
  data() {
    return {
      serverUrl: import.meta.env.VITE_SERVER_DOMAIN,
      serverPort: import.meta.env.VITE_SERVER_PORT,
      inputURL: "",
      inputOffset: "",
      inputCount: "",
      items: [],
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

      this.inputOffset = "";
      this.inputCount = "";

      if (this.items.length === 0) {
        alert("No URLs in the list!");
        return;
      }

      try {
        const requests = this.items.map(url => {
          const encodedURL = encodeURIComponent(url);

          return fetch(`http://${serverUrl}:${serverPort}/parse?url=${encodedURL}&count=${count}&skip=${offset}`)
              .then(response => {
                if (!response.ok) {
                  throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
              });
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
      this.$router.push({ name: "Home" });
    },
  },
}
</script>