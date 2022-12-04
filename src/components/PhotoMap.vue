<template>
  <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true">
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
        <ol-style-icon :src="marker" :scale="0.5"></ol-style-icon>
      </ol-style>
    </ol-vector-layer>

    <ol-interaction-select
      @select="featureSelected"
      :condition="selectCondition"
    >
      <ol-style>
        <ol-style-icon :src="markerSelected" :scale="0.5"></ol-style-icon>
      </ol-style>
    </ol-interaction-select>

    <ol-overlay
      :position="selectedPosition"
      v-if="selectedProperties != null"
      positioning="center"
    >
      <template v-slot="slotProps">
        <div class="bg-black p-3 rounded">
          <h3 class="text-xl text-white">{{ selectedProperties.name }}</h3>
          <p v-if="selectedProperties.desc !== null" class="text-slate-300">
            {{ selectedProperties.desc }}
          </p>
          <p class="text-sm text-slate-500">
            <i class="fa-solid fa-location-dot"></i> {{ selectedProperties.lat }}, {{selectedProperties.lon}}
          </p>
          <div
            v-if="selectedProperties.images.length"
            class="flex mt-3 gap-x-2"
          >
            <span
              v-for="image in selectedProperties.images"
              v-bind:key="image.url"
            >
              <a :href="image.url" target="__blank"
                ><img class="h-28" :src="image.thumbnail"
              /></a>
            </span>
          </div>
        </div>
      </template>
    </ol-overlay>
  </ol-map>
</template>

<script>
import { ref, inject } from "vue";
import { fromLonLat } from "ol/proj";
import { GeoJSON } from "ol/format";

export default {
  name: "photomap",
  props: {
    refcat: String,
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
    };
  },
};
</script>