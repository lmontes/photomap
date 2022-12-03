<template>
    <div class="flex justify-start">
        <!--div class="flex flex-col h-screen p-3 bg-slate-200">
            
        </div-->
        <div class="w-screen h-screen mx-auto">
            <photomap class="w-screen h-screen"></photomap>
        </div>
    </div>
</template>

<script>

import photomap from './components/PhotoMap.vue';

export default {
  components: {photomap}
}

</script>
