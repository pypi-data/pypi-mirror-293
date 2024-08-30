<template>
  <v-autocomplete
    :items="checkOutConditions"
    filled
    v-model="innerValue"
    :prepend-icon="defaultIcons.checkOutCondition"
    :label="$t('plank.check_out_condition.title')"
    item-text="text"
    item-value="id"
    required
    :rules="rules.checkOutCondition"
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "CheckOutConditionInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    checkOutConditions: {
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
