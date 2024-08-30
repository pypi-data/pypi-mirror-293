<template>
  <attribute-row :icon="defaultIcons.status" :label="$t('plank.labels.status')">
    <item-status :item="data"></item-status>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";
import ItemStatus from "../item/ItemStatus.vue";

export default {
  name: "ItemStatusRow",
  components: { ItemStatus, AttributeRow },
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
