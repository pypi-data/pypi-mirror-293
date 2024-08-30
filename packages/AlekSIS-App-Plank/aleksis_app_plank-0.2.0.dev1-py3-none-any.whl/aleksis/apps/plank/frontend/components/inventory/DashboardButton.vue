<template>
  <v-btn
    x-large
    outlined
    class="ma-2 flex-sm-grow-1"
    color="primary"
    v-bind="$attrs"
  >
    <v-icon left v-if="icon">{{ icon }}</v-icon>
    <slot></slot>
  </v-btn>
</template>

<script>
export default {
  name: "DashboardButton",
  props: {
    icon: {
      type: String,
      required: false,
      default: "",
    },
  },
};
</script>
