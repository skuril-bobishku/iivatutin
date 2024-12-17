import { reactive } from 'vue';

export const EventBus = reactive({
    filePath: '',
    projName: '',
    sFilePath(newMessage) {
        this.filePath = newMessage;
    },
    sProjName(newMessage) {
        this.projName = newMessage;
    }
});