<template>
  <attribute-row
    :icon="defaultIcons.serialNumber"
    :label="$t('plank.labels.serial_number')"
  >
    {{ data ? data : "–" }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "SerialNumberRow",
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
