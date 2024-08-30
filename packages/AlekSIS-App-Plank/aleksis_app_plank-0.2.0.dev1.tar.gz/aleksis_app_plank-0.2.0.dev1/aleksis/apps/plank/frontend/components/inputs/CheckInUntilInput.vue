<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    :nudge-right="40"
    transition="scale-transition"
    offset-y
    min-width="auto"
  >
    <template #activator="{ on, attrs }">
      <v-text-field
        v-model="innerValue"
        filled
        :label="$t('plank.labels.check_in_until')"
        :prepend-icon="defaultIcons.date"
        readonly
        :rules="rules.checkInUntil"
        v-bind="attrs"
        v-on="on"
      ></v-text-field>
    </template>
    <v-date-picker v-model="innerValue" @input="menu = false"></v-date-picker>
  </v-menu>
</template>

<script>
import rules from "../../rules";
import defaultIcons from "../../defaultIcons";

export default {
  name: "CheckInUntilInput",
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      rules: rules,
      defaultIcons,
      innerValue: this.value,
      menu: false,
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
