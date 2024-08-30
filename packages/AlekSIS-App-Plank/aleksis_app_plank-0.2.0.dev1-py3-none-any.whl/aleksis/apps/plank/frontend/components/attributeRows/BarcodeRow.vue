<template>
  <attribute-row
    :icon="defaultIcons.barcode"
    :label="$t('plank.labels.barcode')"
  >
    <code>{{ data }}</code>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "BarcodeRow",
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
