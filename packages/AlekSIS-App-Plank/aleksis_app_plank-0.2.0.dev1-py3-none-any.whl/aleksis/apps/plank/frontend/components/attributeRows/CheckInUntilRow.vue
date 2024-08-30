<template>
  <attribute-row
    :icon="defaultIcons.date"
    :label="$t('plank.labels.check_in_until')"
  >
    {{ data ? data : "–" }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "CheckInUntilRow",
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
