<template>
  <div v-if="item.isAvailable">
    <v-chip color="green" text-color="white" label small>
      {{ $t("plank.item.status.available") }}
    </v-chip>

    <span v-if="item.location"> ({{ item.location.name }}) </span>
  </div>
  <div v-else>
    <v-chip color="red" text-color="white" label small>
      {{
        item.currentCheckedOutItem
          ? $t("plank.item.status.checked_out_to")
          : $t("plank.item.status.checked_out")
      }}
    </v-chip>
    <span v-if="item.currentCheckedOutItem">
      <!-- FIXME LINK TO CHECK OUT -->
      <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
      {{ item.currentCheckedOutItem.process.borrowingPerson.fullName }}, #{{
        item.currentCheckedOutItem.process.id
      }}
    </span>
  </div>
</template>

<script>
export default {
  name: "ItemStatus",
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>
