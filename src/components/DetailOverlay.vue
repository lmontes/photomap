<template>
  <div class="bg-black p-3 rounded">
    <h3 class="text-xl text-white">
      <font-awesome-icon :icon="symbolToIcon(properties.symbol)" class="mr-2"/>
      {{properties.name}}
    </h3>
    <p v-if="properties.desc !== null" class="text-slate-300">
      {{properties.desc}}
    </p>
    <p class="text-sm text-slate-500">
      <font-awesome-icon icon="fa-solid fa-location-dot"/> {{properties.lat.toFixed(6)}}, {{properties.lon.toFixed(6)}}
    </p>
    <div v-if="properties.images.length" class="flex mt-3 gap-x-2">
      <span v-for="(image, idx) in properties.images" v-bind:key="image.url">
        <a @click="imageClicked(idx)" >
          <img class="h-28" :src="image.thumbnail"/>
        </a>
      </span>
    </div>
  </div>
</template>

<script>
  export default {
    name: "detail-overlay",
    props: {
      properties: Object,
    },
    methods: {
      imageClicked(index) {
        this.$emit("image-clicked", index);
      },
      symbolToIcon(symbol) {
        var mapping = {
          "House": "fa-solid fa-house",
          "Fountain": "fa-solid fa-faucet",
          "Bridge": "fa-solid fa-archway",
          "Tree": "fa-solid fa-tree",
          "Mountain": "fa-solid fa-mountain",
          "Water": "fa-solid fa-water"
        }

        if (mapping[symbol] !== undefined)
          return mapping[symbol];
        return "fa-solid fa-thumbtack";
      }
    },
    setup(props, context) {}
  };
</script>
