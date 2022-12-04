import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'vue-universal-modal/dist/index.css';
import '@fortawesome/fontawesome-free/css/all.css';

import OpenLayersMap from 'vue3-openlayers'
import 'vue3-openlayers/dist/vue3-openlayers.css'
import VueUniversalModal from 'vue-universal-modal';

const app = createApp(App);

app.use(OpenLayersMap)

app.use(VueUniversalModal, {teleportTarget: '#modals'});

app.mount('#app')
