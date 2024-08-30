<template>
  <attribute-row
    :icon="defaultIcons.manufacturer"
    :label="$t('plank.manufacturer.title')"
  >
    <router-link
      v-if="data"
      :to="{ name: 'plank.manufacturer', params: { id: data.id } }"
      >{{ data.name }}</router-link
    >
    <span v-else>–</span>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "ManufacturerRow",
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
