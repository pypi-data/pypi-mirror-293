<template>
  <attribute-row
    :icon="defaultIcons.itemType"
    :label="$t('plank.item_type.title')"
  >
    <router-link
      v-if="data"
      :to="{ name: 'plank.itemType', params: { id: data.id } }"
      >{{ data.name }}</router-link
    >
    <span v-else>–</span>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "ItemTypeRow",
  components: { AttributeRow },
  props: {
    data: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
