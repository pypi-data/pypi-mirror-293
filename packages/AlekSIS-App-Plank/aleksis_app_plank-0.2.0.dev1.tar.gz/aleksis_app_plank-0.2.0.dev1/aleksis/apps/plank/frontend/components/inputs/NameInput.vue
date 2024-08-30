<template>
  <v-text-field
    filled
    v-model="innerValue"
    :label="$t('plank.labels.name')"
    required
    :counter="255"
    :rules="rules.name"
    prepend-icon="mdi-label-outline"
  ></v-text-field>
</template>

<script>
import rules from "../../rules";

export default {
  name: "NameInput",
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
