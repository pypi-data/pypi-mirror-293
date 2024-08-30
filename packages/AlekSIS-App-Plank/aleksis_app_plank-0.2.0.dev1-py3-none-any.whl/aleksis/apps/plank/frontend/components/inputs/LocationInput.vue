<template>
  <v-autocomplete
    :items="locations"
    filled
    v-model="innerValue"
    :prepend-icon="defaultIcons.location"
    :label="$t('plank.location.title')"
    item-text="name"
    item-value="id"
    :rules="rules.location"
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "LocationInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    locations: {
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
