<template>
  <v-autocomplete
    :items="inventories"
    filled
    v-model="innerValue"
    prepend-icon="mdi-folder-home-outline"
    :label="$t('plank.inventory.title')"
    item-text="name"
    item-value="id"
    required
    :rules="rules.inventory"
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";

export default {
  name: "InventoryInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    inventories: {
      type: Array,
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
