<template>
  <v-autocomplete
    :items="persons"
    filled
    v-model="innerValue"
    :prepend-icon="defaultIcons.person"
    :label="$t('plank.person.title')"
    item-text="fullName"
    item-value="id"
    required
    :rules="rules.person"
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "PersonInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    persons: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      rules: rules,
      defaultIcons,
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
