<template>
  <item-list
    :headers="headers"
    :gql-query="require('./list.graphql')"
    :gql-mutation="require('./mutation.graphql')"
    :gql-delete-mutation="require('./delete.graphql')"
    i18n-key="check_out_process"
    item-attribute="name"
    :default-item="defaultItem"
    :show-create="false"
    v-bind="$attrs"
  >
    <template
      v-for="(_, name) in $scopedSlots"
      :slot="name"
      slot-scope="slotData"
    >
      <slot :name="name" v-bind="slotData" />
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.checkedOutAt="{ item }">
      <router-link
        :to="{ name: 'plank.checkOutProcess', params: { id: item.id } }"
      >
        {{ item.checkedOutAt }}
      </router-link>
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.status="{ item }">
      <check-out-process-status :check-out-process="item" />
    </template>
    <template #fields="{ currentItem }">
      <!-- eslint-disable-next-line vue/valid-v-model -->
      <check-out-process-fields v-model="currentItem" :form-data="formData" />
    </template>
  </item-list>
</template>

<script>
import rules from "../../rules";
import ItemList from "../ItemList.vue";
import defaultItems from "../../defaultItems";
import CheckOutProcessFields from "./CheckOutProcessFields.vue";
import CheckOutProcessStatus from "./CheckOutProcessStatus.vue";

import gqlFormData from "./formData.graphql";
export default {
  name: "CheckOutProcessBaseList",
  components: {
    CheckOutProcessStatus,
    CheckOutProcessFields,
    ItemList,
  },
  apollo: {
    formData: {
      query: gqlFormData,
      result({ data }) {
        if (data) {
          this.formData = data;
        }
      },
    },
  },
  computed: {
    headers() {
      return [
        {
          text: this.$t("plank.labels.id"),
          value: "id",
        },
        {
          text: this.$t("plank.inventory.title"),
          value: "inventory.name",
        },
        { text: this.$t("plank.labels.checked_out_at"), value: "checkedOutAt" },
        {
          text: this.$t("plank.labels.lending_person"),
          value: "lendingPerson.fullName",
        },
        {
          text: this.$t("plank.labels.borrowing_person"),
          value: "borrowingPerson.fullName",
        },
        { text: this.$t("plank.item.title_plural"), value: "itemsCount" },
        {
          text: this.$t("plank.labels.status"),
          value: "status",
        },
      ];
    },
  },
  data() {
    return {
      defaultItem: defaultItems.checkOutProcess,
      rules: rules,
      formData: {
        checkOutConditions: [],
      },
    };
  },
};
</script>
