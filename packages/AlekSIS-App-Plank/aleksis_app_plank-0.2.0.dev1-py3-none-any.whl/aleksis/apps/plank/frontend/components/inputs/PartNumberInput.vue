<template>
  <v-text-field
    filled
    v-model="innerValue"
    :label="$t('plank.labels.part_number')"
    :counter="255"
    :rules="rules.partNumber"
    :prepend-icon="defaultIcons.partNumber"
  ></v-text-field>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "PartNumberInput",
  props: {
    value: {
      type: String,
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
