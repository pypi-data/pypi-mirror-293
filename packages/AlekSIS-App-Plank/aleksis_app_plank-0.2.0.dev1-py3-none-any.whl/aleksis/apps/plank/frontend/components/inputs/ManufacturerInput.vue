<template>
  <v-autocomplete
    :items="manufacturers"
    filled
    v-model="innerValue"
    :prepend-icon="defaultIcons.manufacturer"
    :label="$t('plank.manufacturer.title')"
    item-text="name"
    item-value="id"
    required
    :rules="rules.manufacturer"
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "ManufacturerInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    manufacturers: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      rules: rules,
      defaultIcons: defaultIcons,
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
