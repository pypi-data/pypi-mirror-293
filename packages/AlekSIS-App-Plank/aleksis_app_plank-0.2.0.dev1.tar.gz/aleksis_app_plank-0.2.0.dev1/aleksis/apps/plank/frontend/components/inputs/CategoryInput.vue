<template>
  <v-autocomplete
    :items="categories"
    filled
    v-model="innerValue"
    :prepend-icon="defaultIcons.category"
    :label="$t('plank.category.title')"
    item-text="name"
    item-value="id"
    required
    :rules="rules.category"
    auto-select-first
  ></v-autocomplete>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "CategoryInput",
  props: {
    value: {
      type: String,
      required: false,
      default: "",
    },
    categories: {
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
