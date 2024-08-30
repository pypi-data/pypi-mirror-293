<template>
  <attribute-row
    :icon="defaultIcons.inventory"
    :label="$t('plank.inventory.title')"
  >
    <router-link :to="{ name: 'plank.inventory', params: { id: data.id } }">{{
      data.name
    }}</router-link>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "InventoryRow",
  components: { AttributeRow },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
