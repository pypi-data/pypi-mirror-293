<template>
  <v-autocomplete
    :items="icons"
    filled
    v-model="innerValue"
    :prepend-icon="innerValue ? 'mdi-' + innerValue : 'mdi-select-remove'"
    :label="$t('plank.labels.icon')"
    clearable
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";

export default {
  name: "IconInput",
  props: {
    value: {
      type: String,
      required: true,
    },
    icons: {
      type: Array,
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
