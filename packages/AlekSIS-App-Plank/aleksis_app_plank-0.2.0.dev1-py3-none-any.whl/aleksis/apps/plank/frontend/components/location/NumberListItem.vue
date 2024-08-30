<template>
  <v-list-item>
    <v-list-item-icon>
      <v-icon :color="iconColor">{{ icon }}</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title><slot name="title"></slot></v-list-item-title>
    </v-list-item-content>
    <v-list-item-action class="text-right text-h5">{{
      data
    }}</v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  name: "NumberListItem",
  props: {
    icon: {
      type: String,
      required: true,
    },
    iconColor: {
      type: String,
      required: false,
      default: "primary",
    },
    data: {
      type: Number,
      required: true,
    },
  },
};
</script>
