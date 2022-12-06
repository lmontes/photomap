<template>
    <ol-map class="w-screen h-screen mx-auto" :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true">
      <ol-view
        ref="view"
        :center="center"
        :rotation="rotation"
        :zoom="zoom"
        :projection="projection"
      />

      <ol-tile-layer :minZoom="1" :mapMaxZoom="minZoom">
        <ol-source-osm />
      </ol-tile-layer>

      <ol-tile-layer
        v-if="mapSource == 'sigpac'"
        :minZoom="minZoom"
        :mapMaxZoom="mapMaxZoom"
      >
        <ol-source-wmts
          :attributions="attribution"
          :url="url"
          :matrixSet="matrixSet"
          :format="format"
          :layer="layerName"
          :style="styleName"
        >
        </ol-source-wmts>
      </ol-tile-layer>

      <ol-fullscreen-control />
      <ol-scaleline-control />
      <ol-zoom-control />

      <ol-vector-layer :minZoom="minZoom" :mapMaxZoom="mapMaxZoom">
        <ol-source-vector ref="source" url="data/data.geojson" :format="geoJson">
          <ol-interaction-snap />
        </ol-source-vector>
        <ol-style>
          <ol-style-icon :src="marker" :scale="0.4"></ol-style-icon>
        </ol-style>
      </ol-vector-layer>

      <ol-interaction-select
        @select="featureSelected"
        :condition="selectCondition"
      >
        <ol-style>
          <ol-style-icon :src="markerSelected" :scale="0.4"></ol-style-icon>
        </ol-style>
      </ol-interaction-select>

      <ol-overlay
        :position="selectedPosition"
        v-if="selectedProperties != null"
        positioning="top-center"
      >
        <detail-overlay :properties="selectedProperties" @image-clicked="showModal">
        </detail-overlay>
      </ol-overlay>
    </ol-map>
    <Modal v-model="viewModal" :close="closeModal">
      <photo-viewer :images="selectedProperties.images" :close="closeModal" :index="imageIndex">
      </photo-viewer>
    </Modal>
</template>

<script>
import { ref, inject } from "vue";
import { fromLonLat } from "ol/proj";
import { GeoJSON } from "ol/format";
import DetailOverlay from './DetailOverlay.vue';
import PhotoViewer from "./PhotoViewer.vue";

export default {
  name: "photomap",
  props: {},
  components: {
    DetailOverlay,
    PhotoViewer
  },
  methods: {
    showModal(index) {
      this.imageIndex = index;
      this.viewModal = true;
    },
    closeModal() {
      this.viewModal = false;
    }
  },
  setup(props, context) {
    const view = ref(null);
    const source = ref(null);

    const projection = ref("EPSG:3857");
    const minZoom = ref(11);
    const mapMaxZoom = ref(20);
    const center = fromLonLat([-1.1656058, 39.51562118]);
    const zoom = ref(13);
    const rotation = ref(0);

    // WMTS SIGPAC
    const url = ref("https://sigpac.mapama.gob.es/SDG/wmts");
    const layerName = ref("ortofotos");
    const matrixSet = ref("EPSG3857");
    const format = ref("image/jpeg");
    const styleName = ref("default");
    const attribution = ref(
      'Tiles © <a href="https://sigpac.mapama.gob.es" target="_blank">SIGPAC</a>'
    );

    const geoJson = new GeoJSON();

    // Seleccion de elementos al hacer click
    const extent = inject("ol-extent");
    const selectConditions = inject("ol-selectconditions");
    const selectCondition = selectConditions.click;

    const selectedProperties = ref(null);
    const selectedPosition = ref([]);

    const featureSelected = (event) => {
      //console.log(event);
      if (event.selected.length == 1) {
        selectedPosition.value = extent.getCenter(
          event.selected[0].getGeometry().extent_
        );
        selectedProperties.value = event.selected[0].values_;
      } else {
        selectedProperties.value = null;
      }
    };

    const marker = ref("icons/marker.png");
    const markerSelected = ref("icons/marker-selected.png");

    const mapSource = ref("sigpac"); // "sigpac"

    const viewModal = ref(false);
    const imageIndex = ref(0);

    return {
      projection,
      center,
      zoom,
      rotation,
      url,
      layerName,
      matrixSet,
      format,
      styleName,
      attribution,
      minZoom,
      mapMaxZoom,
      geoJson,
      view,
      source,
      selectedProperties,
      selectedPosition,
      featureSelected,
      selectCondition,
      marker,
      markerSelected,
      mapSource,
      viewModal,
      imageIndex
    };
  },
};
</script>