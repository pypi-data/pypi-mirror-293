<template>
  <v-textarea
    filled
    v-model="innerValue"
    :label="$t('plank.labels.description')"
    auto-grow
    prepend-icon="mdi-comment-outline"
  />
</template>

<script>
import rules from "../../rules";

export default {
  name: "DescriptionInput",
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      rules: rules,
      innerValue: this.value,
    };
  },
  watch: {
    value(val) {
      this.innerValue = val;
    },
    innerValue(val) {
      this.$emit("input", val);
    },
  },
};
</script>
