<template>
  <attribute-row
    :icon="defaultIcons.lastTimeSeenAt"
    :label="$t('plank.labels.last_time_seen_at')"
  >
    {{ data ? data : "–" }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "LastTimeSeenAtRow",
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
