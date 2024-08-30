<template>
  <item-list
    :headers="headers"
    :gql-query="require('./list.graphql')"
    :gql-mutation="require('./mutation.graphql')"
    :gql-delete-mutation="require('./delete.graphql')"
    i18n-key="category"
    item-attribute="name"
    :default-item="defaultItem"
    :show-create="formData.canCreate"
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
    <template #item.name="{ item }">
      <category-chip :category="item" />
    </template>
    <template #fields="{ currentItem }">
      <!-- eslint-disable-next-line vue/valid-v-model -->
      <category-fields v-model="currentItem" :form-data="formData" />
    </template>
  </item-list>
</template>

<script>
import rules from "../../rules";
import ItemList from "../ItemList.vue";
import defaultItems from "../../defaultItems";
import CategoryChip from "./CategoryChip.vue";
import CategoryFields from "./CategoryFields.vue";
import gqlFormData from "./formData.graphql";

export default {
  name: "CategoryBaseList",
  components: {
    CategoryFields,
    ItemList,
    CategoryChip,
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
        { text: this.$t("plank.labels.name"), value: "name" },
        { text: this.$t("plank.item.title_plural"), value: "itemsCount" },
        {
          text: this.$t("plank.item_type.title_plural"),
          value: "itemTypesCount",
        },
      ];
    },
  },
  data() {
    return {
      defaultItem: defaultItems.category,
      rules: rules,
      formData: {
        icons: [],
        canCreate: false,
      },
    };
  },
};
</script>
