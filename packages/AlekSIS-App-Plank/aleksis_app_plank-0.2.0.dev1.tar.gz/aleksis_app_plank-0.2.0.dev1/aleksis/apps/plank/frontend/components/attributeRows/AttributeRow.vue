<template>
  <tr>
    <td>
      <v-icon v-if="icon" color="primary" left class="mr-4">{{ icon }}</v-icon>
      <strong>{{ label }}</strong>
    </td>
    <td>
      <slot></slot>
    </td>
  </tr>
</template>

<script>
export default {
  name: "AttributeRow",
  props: {
    icon: {
      type: String,
      required: false,
      default: "",
    },
    label: {
      type: String,
      required: true,
    },
  },
};
</script>
