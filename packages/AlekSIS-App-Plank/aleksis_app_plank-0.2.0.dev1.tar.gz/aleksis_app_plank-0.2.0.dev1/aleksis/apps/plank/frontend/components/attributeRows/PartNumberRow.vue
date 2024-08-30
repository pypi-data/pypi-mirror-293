<template>
  <attribute-row
    :icon="defaultIcons.partNumber"
    :label="$t('plank.labels.part_number')"
  >
    {{ data ? data : "–" }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "PartNumberRow",
  components: { AttributeRow },
  props: {
    data: {
      type: String,
      required: false,
      default: "",
    },
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
