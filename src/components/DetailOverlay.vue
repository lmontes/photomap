<template>
  <div class="bg-black p-3 rounded">
    <h3 class="text-xl text-white">{{ properties.name }}</h3>
    <p v-if="properties.desc !== null" class="text-slate-300">
      {{ properties.desc }}
    </p>
    <p class="text-sm text-slate-500">
      <i class="fa-solid fa-location-dot"></i> {{ properties.lat }}, {{properties.lon}}
    </p>
    <div v-if="properties.images.length" class="flex mt-3 gap-x-2">
      <span v-for="image in properties.images" v-bind:key="image.url">
        <a :href="image.url" target="__blank">
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
    setup(props, context) {}
  };
</script>
