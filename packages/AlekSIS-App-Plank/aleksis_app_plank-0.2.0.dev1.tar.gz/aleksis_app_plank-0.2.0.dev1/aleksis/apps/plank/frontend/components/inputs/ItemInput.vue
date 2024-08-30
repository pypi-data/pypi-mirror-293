<template>
  <v-autocomplete
    :items="items"
    filled
    v-model="innerValue"
    :prepend-icon="defaultIcons.item"
    :label="$t('plank.item.title')"
    :item-text="(item) => `${item.name} (${item.id})`"
    item-value="id"
    :rules="rules.item"
    auto-select-first
    clearable
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "ItemInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    items: {
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
