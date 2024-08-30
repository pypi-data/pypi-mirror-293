<template>
  <span>
    <v-icon v-if="status === 'in_place'" color="green">mdi-check</v-icon>
    <v-icon v-else-if="status === 'moved'">mdi-plus</v-icon>
  </span>
</template>

<script>
export default {
  name: "LocationItemStatusIcon",
  computed: {
    status() {
      if (this.item && this.item.id in this.itemStatuses) {
        return this.itemStatuses[this.item.id];
      }
      return null;
    },
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    itemStatuses: {
      type: Object,
      required: false,
      default: () => {},
    },
  },
};
</script>
