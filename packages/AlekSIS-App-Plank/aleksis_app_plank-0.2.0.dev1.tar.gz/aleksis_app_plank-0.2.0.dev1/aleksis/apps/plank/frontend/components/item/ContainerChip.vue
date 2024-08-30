<script>
export default {
  name: "ContainerChip",
};
</script>

<template>
  <v-chip label small outlined color="purple" v-bind="$attrs">
    {{ $t("plank.item.container") }}
  </v-chip>
</template>

<style scoped></style>
