import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'vue-universal-modal/dist/index.css';
import OpenLayersMap from 'vue3-openlayers'
import 'vue3-openlayers/dist/vue3-openlayers.css'
import VueUniversalModal from 'vue-universal-modal';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { 
    faLocationDot,
    faHome,
    faFaucet,
    faArchway,
    faThumbTack,
    faTree,
    faMountain,
    faWater,
    faChevronLeft,
    faChevronRight,
    faXmark
} from '@fortawesome/free-solid-svg-icons';

const app = createApp(App);

app.use(OpenLayersMap)

library.add([
    faLocationDot,
    faHome,
    faFaucet,
    faArchway,
    faThumbTack,
    faTree,
    faMountain,
    faWater,
    faChevronLeft,
    faChevronRight,
    faXmark
]);
app.component('font-awesome-icon', FontAwesomeIcon);

app.use(VueUniversalModal, {teleportTarget: '#modals'});

app.mount('#app')
