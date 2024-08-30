<template>
  <v-chip :color="category.colour">
    <v-icon v-if="category.icon" left>mdi-{{ category.icon }}</v-icon>
    {{ category.name }}
  </v-chip>
</template>

<script>
export default {
  name: "CategoryChip",
  props: {
    category: {
      type: Object,
      required: true,
    },
  },
};
</script>
