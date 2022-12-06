<template>
  <div class="mx-auto max-w-6xl">
    <div class="relative">
      <div class="p-2 bg-white">
        <img class="w-full object-cover" :src="images[currentIndex].url" />
        <div v-if="images[currentIndex].name"
          class="
            text-center text-white
            font-light
            tracking-wider
            bg-gray-800
            py-2
          "
        >
          <p id="caption">
            {{images[currentIndex].name}}
          </p>
        </div>
      </div>
      <a
        v-if="this.currentIndex > 0"
        class="
          absolute
          left-0
          inset-y-0
          flex
          items-center
          px-4
          text-white
          hover:text-gray-800
          cursor-pointer
          text-4xl
          font-extrabold
        "
        @click="next(-1)"
      >
        <i class="fa-solid fa-chevron-left"></i>
      </a>
      <a
        v-if="this.currentIndex < this.images.length - 1"
        class="
          absolute
          right-0
          inset-y-0
          flex
          items-center
          px-4
          text-white
          hover:text-gray-800
          cursor-pointer
          text-4xl
          font-extrabold
        "
        @click="next(1)"
      >
        <i class="fa-solid fa-chevron-right"></i>
      </a>
      <a
        class="
          absolute
          right-0
          inset-x-0
          top-0
          grid
          justify-items-end
          m-4
          text-white
          hover:text-gray-800
          cursor-pointer
          text-4xl
          font-extrabold
        "
        @click="close"
      >
        <i class="fa-solid fa-xmark"></i>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "photo-viewer",
  props: {
    images: Array,
    index: Number,
    close: Function,
  },
  data() {
    return {
      currentIndex: this.index,
    };
  },
  methods: {
    next(n) {
      if (
        this.currentIndex + n >= 0 &&
        this.currentIndex + n < this.$props.images.length
      )
        this.currentIndex += n;
    },
  },
};
</script>
