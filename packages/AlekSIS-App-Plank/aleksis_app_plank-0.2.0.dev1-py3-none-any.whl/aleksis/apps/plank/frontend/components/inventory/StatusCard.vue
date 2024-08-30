<template>
  <v-card outlined :color="color">
    <v-card-text>
      <div :class="'text-h2 text-center ' + this.textColor">
        {{ number }}
      </div>
      <div :class="'text-body-1 text-center ' + this.textColor">
        {{ title }}
      </div>
    </v-card-text>
    <v-card-actions>
      <slot name="actions"></slot>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "StatusCard",
  computed: {
    textColor() {
      return this.color ? "white--text" : "";
    },
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    number: {
      type: [String, Number],
      required: true,
    },
    color: {
      type: String,
      required: false,
      default: "",
    },
  },
};
</script>
