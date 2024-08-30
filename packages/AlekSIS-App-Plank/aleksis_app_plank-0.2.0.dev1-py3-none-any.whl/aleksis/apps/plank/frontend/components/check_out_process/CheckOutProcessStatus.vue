<template>
  <v-chip
    color="green"
    text-color="white"
    label
    small
    v-if="checkOutProcess.isEverythingCheckedIn"
  >
    {{ $t("plank.check_out_process.status.checked_in") }}
  </v-chip>
  <v-chip
    color="orange"
    text-color="white"
    label
    small
    v-else-if="checkOutProcess.isInTime"
  >
    {{ $t("plank.check_out_process.status.checked_out") }}
  </v-chip>
  <v-chip color="red" text-color="white" label small v-else>
    {{ $t("plank.check_out_process.status.not_in_time") }}
  </v-chip>
</template>

<script>
export default {
  name: "CheckOutProcessStatus",
  props: {
    checkOutProcess: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>
