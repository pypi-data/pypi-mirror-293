<template>
  <item-list
    :headers="headers"
    :gql-query="require('./list.graphql')"
    :gql-mutation="require('./mutation.graphql')"
    :gql-delete-mutation="require('./delete.graphql')"
    i18n-key="item_type"
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
    <template #item.category.name="{ item }">
      <category-chip :category="item.category" />
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.manufacturer.name="{ item }">
      {{ item.manufacturer ? item.manufacturer.name : "–" }}
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.name="{ item }">
      <router-link :to="{ name: 'plank.itemType', params: { id: item.id } }">
        {{ item.name }}
      </router-link>
    </template>
    <template #fields="{ currentItem }">
      <!-- eslint-disable-next-line vue/valid-v-model -->
      <item-type-fields v-model="currentItem" :form-data="formData" />
    </template>
  </item-list>
</template>

<script>
import rules from "../../rules";
import ItemList from "../ItemList.vue";
import defaultItems from "../../defaultItems";
import CategoryChip from "../category/CategoryChip.vue";
import ItemTypeFields from "./ItemTypeFields.vue";
import gqlFormData from "./formData.graphql";

export default {
  name: "BaseItemTypeList",
  components: { ItemTypeFields, ItemList, CategoryChip },
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
          text: this.$t("plank.category.title"),
          value: "category.name",
        },
        {
          text: this.$t("plank.manufacturer.title"),
          value: "manufacturer.name",
        },
        { text: this.$t("plank.labels.name"), value: "name" },
        {
          text: this.$t("plank.item.title_plural"),
          value: "itemsCount",
        },
      ];
    },
  },
  data() {
    return {
      defaultItem: defaultItems.itemType,
      rules: rules,
      formData: {
        manufactures: [],
        categories: [],
        canCreate: false,
      },
    };
  },
};
</script>
