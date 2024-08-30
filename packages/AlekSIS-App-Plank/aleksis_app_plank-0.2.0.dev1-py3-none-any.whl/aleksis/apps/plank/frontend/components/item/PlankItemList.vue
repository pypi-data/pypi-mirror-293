<template>
  <item-base-list :hide-columns="['locationStatus']"></item-base-list>
</template>

<script>
import ItemBaseList from "./ItemBaseList.vue";

export default {
  name: "PlankItemList",
  components: { ItemBaseList },
};
</script>
