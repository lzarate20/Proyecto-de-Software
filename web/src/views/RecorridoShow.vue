<template>
  <span class="item1">{{ recorrido.nombre }}</span>
  <span v-if="show" @click="changeShow" class="item2 item2b page-link" style="width: fit-content; margin: auto;">Mostrar menos</span>
  <span v-else @click="changeShow" class="item2 item2b page-link" style="width: fit-content; margin: auto;">Mostrar mas</span>
  <div v-if="show" class="box item3">
    <span>Descripcion:{{ recorrido.descripcion }}</span>
  </div>
</template>
<script>
export default {
  props: {
    recorrido: Object,
  },
  data() {
    return {
      show: false,
    };
  },
  methods: {
    changeShow() {
      this.show = !this.show;
    },
  },
};
</script>


