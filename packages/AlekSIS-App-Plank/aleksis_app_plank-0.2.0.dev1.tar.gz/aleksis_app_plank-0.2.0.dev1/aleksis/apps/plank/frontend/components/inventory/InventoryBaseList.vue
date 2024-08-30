<template>
  <item-list
    :headers="headers"
    :gql-query="require('./list.graphql')"
    :gql-mutation="require('./mutation.graphql')"
    :gql-delete-mutation="require('./delete.graphql')"
    i18n-key="inventory"
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
      <router-link :to="{ name: 'plank.inventory', params: { id: item.id } }">
        {{ item.name }}
      </router-link>
    </template>
    <template #fields="{ currentItem }">
      <name-input v-model="currentItem.name" />
      <groups-input
        v-model="currentItem.checkOutGroups"
        :groups="formData.groups"
        :label="$t('plank.labels.check_out_groups')"
      />
      <group-input
        v-model="currentItem.checkOutCreateGroup"
        :groups="formData.groups"
        :label="$t('plank.labels.check_out_create_group')"
      />
    </template>
  </item-list>
</template>

<script>
import rules from "../../rules";
import ItemList from "../ItemList.vue";
import defaultItems from "../../defaultItems";
import NameInput from "../inputs/NameInput.vue";
import GroupsInput from "../inputs/GroupsInput.vue";
import GroupInput from "../inputs/GroupInput.vue";
import gqlFormData from "./formData.graphql";
export default {
  name: "InventoryBaseList",
  components: { GroupInput, GroupsInput, NameInput, ItemList },
  apollo: {
    formData: {
      query: gqlFormData,
      result({ data }) {
        if (data) {
          this.formData = data;
        }
      },
      manual: true,
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
      ];
    },
  },
  data() {
    return {
      defaultItem: defaultItems.inventory,
      rules: rules,
      formData: {
        canCreate: false,
      },
    };
  },
};
</script>
