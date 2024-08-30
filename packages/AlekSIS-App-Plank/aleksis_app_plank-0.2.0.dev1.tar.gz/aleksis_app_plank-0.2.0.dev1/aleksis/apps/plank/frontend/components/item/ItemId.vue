<template>
  <span
    >{{ item.id }} (<code>{{ item.barcode }}</code
    >)</span
  >
</template>

<script>
import defaultIcons from "../../defaultIcons";

export default {
  name: "ItemId",
  data() {
    return { defaultIcons };
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
};
</script>
