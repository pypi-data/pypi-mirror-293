<template>
  <v-data-table
    :headers="headers"
    :items="items"
    class="elevation-1"
    :items-per-page="100"
  >
    <template #top>
      <v-toolbar flat>
        <v-toolbar-title>
          <v-icon left>{{ defaultIcons.checkOut }}</v-icon>
          {{ $t("plank.check_out.title_plural") }}
        </v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
      </v-toolbar>
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.actions="{ item }">
      <v-btn text color="primary">
        {{ $t("plank.actions.show_more") }}
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import defaultIcons from "../../defaultIcons";

export default {
  name: "CheckOutHistoryTable",
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
  computed: {
    headers() {
      return [
        {
          value: "process.id",
          text: this.$t("plank.labels.id"),
        },
        {
          value: "process.checkedOutAt",
          text: this.$t("plank.labels.checked_out_at"),
        },
        {
          value: "checkedInAt",
          text: this.$t("plank.labels.checked_in_at"),
        },
        {
          value: "process.borrowingPerson.fullName",
          text: this.$t("plank.labels.borrowing_person"),
        },
        {
          value: "actions",
          text: this.$t("plank.actions.title"),
          sortable: false,
        },
        // FIXME ACtions column with link
      ];
    },
  },
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>
