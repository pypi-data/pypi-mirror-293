<template>
  <v-autocomplete
    :items="groups"
    filled
    v-model="innerValue"
    prepend-icon="mdi-account-multiple-plus-outline"
    :label="label || $t('plank.group.title')"
    item-text="name"
    item-value="id"
    clearable
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";

export default {
  name: "GroupInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    groups: {
      type: Array,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: "",
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
