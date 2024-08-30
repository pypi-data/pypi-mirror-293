<template>
  <item-list
    :headers="headers"
    :gql-query="require('./list.graphql')"
    :gql-mutation="require('./mutation.graphql')"
    :gql-delete-mutation="require('./delete.graphql')"
    i18n-key="manufacturer"
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
      <router-link
        :to="{ name: 'plank.manufacturer', params: { id: item.id } }"
      >
        {{ item.name }}
      </router-link>
    </template>
    <template #fields="{ currentItem }">
      <name-input v-model="currentItem.name" />
      <notes-input v-model="currentItem.notes" />
    </template>
  </item-list>
</template>

<script>
import rules from "../../rules";
import ItemList from "../ItemList.vue";
import defaultItems from "../../defaultItems";
import NameInput from "../inputs/NameInput.vue";
import NotesInput from "../inputs/NotesInput.vue";
import gqlFormData from "./formData.graphql";

export default {
  name: "ManufacturerBaseList",
  components: { NotesInput, NameInput, ItemList },
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
      defaultItem: defaultItems.manufacturer,
      rules: rules,
      formData: {
        canCreate: false,
      },
    };
  },
};
</script>
