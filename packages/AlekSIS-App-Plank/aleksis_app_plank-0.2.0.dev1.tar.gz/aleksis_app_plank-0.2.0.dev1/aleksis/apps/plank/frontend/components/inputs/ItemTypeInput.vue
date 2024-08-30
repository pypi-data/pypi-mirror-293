<template>
  <v-autocomplete
    :items="itemTypes"
    filled
    v-model="innerValue"
    :prepend-icon="defaultIcons.itemType"
    :label="$t('plank.item_type.title')"
    item-text="name"
    item-value="id"
    :rules="rules.itemType"
    auto-select-first
    clearable
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "ItemTypeInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    itemTypes: {
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
