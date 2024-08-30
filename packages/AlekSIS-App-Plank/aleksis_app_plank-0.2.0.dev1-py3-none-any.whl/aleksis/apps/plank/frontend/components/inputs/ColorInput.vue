<template>
  <v-color-picker v-model="innerValue" mode="hexa"></v-color-picker>
</template>

<script>
import rules from "../../rules";

export default {
  name: "ColorInput",
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
