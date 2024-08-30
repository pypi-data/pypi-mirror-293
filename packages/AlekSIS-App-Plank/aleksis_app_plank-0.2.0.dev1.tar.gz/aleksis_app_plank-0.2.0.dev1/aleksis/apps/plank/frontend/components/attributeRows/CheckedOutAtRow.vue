<template>
  <attribute-row
    :icon="defaultIcons.checkedOutAt"
    :label="$t('plank.labels.checked_out_at')"
  >
    {{ data ? data : "–" }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "CheckedOutAtRow",
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
