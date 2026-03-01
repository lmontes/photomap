<template>
  <ol-map class="w-screen h-screen mx-auto" :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true">
    <ol-view
      ref="view"
      :center="center"
      :rotation="rotation"
      :zoom="zoom"
      :projection="projection"
    />

    <!-- Capa WMTS OSM -->
    <ol-tile-layer :minZoom="minZoom" :maxZoom="maxZoom" :zIndex="0" title="OSM">
      <ol-source-osm />
    </ol-tile-layer>
    <!-- Capa WMTS IGN (PNOA) -->
    <ol-tile-layer v-if="wmtsOptions" :minZoom="minZoom" :maxZoom="maxZoom" :zIndex="0" title="IGN (PNOA)">
      <ol-source-wmts v-bind="wmtsOptions" />
    </ol-tile-layer>

    <ol-full-screen-control />
    <ol-scale-line-control />
    <ol-zoom-control />
    <ol-layer-switcher-control :displayInLayerSwitcher="displayInLayerSwitcher" />

    <ol-vector-layer :minZoom="minZoom" :maxZoom="maxZoom" :zIndex="1">
      <ol-source-vector ref="source" url="data/data.geojson" :format="geoJson">
        <ol-interaction-snap />
      </ol-source-vector>
      <ol-style>
        <ol-style-icon :src="marker" :scale="0.4"></ol-style-icon>
      </ol-style>
    </ol-vector-layer>

    <ol-interaction-select @select="featureSelected" :condition="selectCondition">
      <ol-style>
        <ol-style-icon :src="markerSelected" :scale="0.4"></ol-style-icon>
      </ol-style>
    </ol-interaction-select>

    <ol-overlay v-if="selectedProperties != null" :position="selectedPosition" positioning="top-center">
      <detail-overlay :properties="selectedProperties" @image-clicked="showModal" />
    </ol-overlay>
  </ol-map>
  <Modal v-model="viewModal" :close="closeModal">
    <photo-viewer :images="selectedProperties.images" :close="closeModal" :index="imageIndex" />
  </Modal>
</template>

<script setup>
import { ref, inject, onMounted } from "vue";
import { fromLonLat } from "ol/proj";
import { GeoJSON } from "ol/format";
import { optionsFromCapabilities } from "ol/source/WMTS";
import WMTSCapabilities from "ol/format/WMTSCapabilities";
import DetailOverlay from "./DetailOverlay.vue";
import PhotoViewer from "./PhotoViewer.vue";

const props = defineProps({});

const projection = ref("EPSG:3857");
const minZoom = ref(11);
const maxZoom = ref(20);
const center = ref(fromLonLat([-1.1656058, 39.51562118]));
const zoom = ref(13);
const rotation = ref(0);

const geoJson = new GeoJSON({
  featureProjection: projection.value,
});

const extent = inject("ol-extent");
const selectConditions = inject("ol-selectconditions");
const selectCondition = selectConditions.click;

const selectedProperties = ref(null);
const selectedPosition = ref([]);
const marker = ref("icons/marker.png");
const markerSelected = ref("icons/marker-selected.png");

const viewModal = ref(false);
const imageIndex = ref(0);

const showModal = (index) => {
  imageIndex.value = index;
  viewModal.value = true;
};

const closeModal = () => {
  viewModal.value = false;
};

const featureSelected = (event) => {
  if (event.selected.length === 1) {
    selectedPosition.value = extent.getCenter(
      event.selected[0].getGeometry().extent_
    );
    selectedProperties.value = event.selected[0].values_;
  } else {
    selectedProperties.value = null;
  }
};

const displayInLayerSwitcher = (layer) => {
  return layer.get("title") !== undefined;
};

const wmtsOptions = ref(null);

onMounted(async () => {
  const response = await fetch(
    "https://www.ign.es/wmts/pnoa-ma?Service=WMTS&Request=GetCapabilities&Version=1.0.0"
  );
  const text = await response.text();
  const parser = new WMTSCapabilities();
  const result = parser.read(text);
  const options = optionsFromCapabilities(result, {
    layer: "OI.OrthoimageCoverage",
    matrixSet: "GoogleMapsCompatible",
  });

  if (options) {
    options.attributions =
      'Tiles © <a href="https://www.ign.es" target="_blank">IGN</a>';
    wmtsOptions.value = options;
    const resolutions = options.tileGrid.getResolutions();
    maxZoom.value = resolutions.length - 1;
  }
});
</script>
