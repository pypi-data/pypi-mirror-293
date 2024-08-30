<template>
  <v-autocomplete
    :items="groups"
    filled
    v-model="innerValue"
    prepend-icon="mdi-account-group-outline"
    :label="label || $t('plank.group.title_plural')"
    item-text="name"
    item-value="id"
    multiple
    clearable
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";

export default {
  name: "GroupsInput",
  props: {
    value: {
      type: Array,
      required: false,
      default: () => [],
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
