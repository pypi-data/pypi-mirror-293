<template>
  <attribute-row :icon="defaultIcons.notes" :label="$t('plank.labels.notes')">
    <span style="white-space: pre-line">{{ data ? data : "–" }}</span>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "NotesRow",
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
