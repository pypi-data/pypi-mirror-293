<template>
  <v-chip outlined color="primary">
    <v-icon left>{{ defaultIcons.item }}</v-icon>
    <item-label :item="item" />
  </v-chip>
</template>

<script>
import defaultIcons from "../../defaultIcons";
import ItemLabel from "./ItemLabel.vue";

export default {
  name: "ItemChip",
  components: { ItemLabel },
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
