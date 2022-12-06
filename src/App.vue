<template>
  <div class="flex justify-start">
    <div class="w-screen h-screen mx-auto">
      <photomap></photomap>
      <!--div class="relative">
        <button class="
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
          bg-black
          text-white
        ">Hahah</button>
      </div-->
    </div>
  </div>
</template>

<script>
import photomap from './components/PhotoMap.vue';

export default {
  components: {photomap}
}
</script>
