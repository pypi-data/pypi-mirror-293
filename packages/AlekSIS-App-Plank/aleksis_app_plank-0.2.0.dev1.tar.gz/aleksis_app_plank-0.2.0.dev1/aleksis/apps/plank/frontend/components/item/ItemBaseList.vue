<template>
  <item-list
    :headers="headers"
    :gql-query="require('./list.graphql')"
    :gql-mutation="require('./mutation.graphql')"
    :gql-delete-mutation="require('./delete.graphql')"
    i18n-key="item"
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
    <template #item.locationStatus="{ item }">
      <v-fade-transition>
        <location-item-status-icon :item="item" :item-statuses="itemStatuses" />
      </v-fade-transition>
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.id="{ item }">
      <item-id :item="item" />
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.category.name="{ item }">
      <category-chip :category="item.category" />
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.itemType.name="{ item }">
      {{ item.itemType ? item.itemType.name : "–" }}
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.name="{ item }">
      <router-link :to="{ name: 'plank.item', params: { id: item.id } }">
        {{ item.name }}
      </router-link>

      <container-chip
        v-if="item.isLocation"
        :to="{ name: 'plank.location', params: { id: item.isLocation.id } }"
        class="ml-2"
      />
    </template>
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #item.status="{ item }">
      <item-status :item="item" />
    </template>
    <template #fields="{ currentItem }">
      <scan-input v-model="currentItem.barcode" />
      <category-input
        v-model="currentItem.category"
        :categories="formData.categories"
      />
      <item-type-input
        v-model="currentItem.itemType"
        :item-types="formData.itemTypes"
      />
      <name-input v-model="currentItem.name" />
      <location-input
        v-model="currentItem.location"
        :locations="formData.locations"
      />
      <serial-number-input v-model="currentItem.serialNumber" />
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
import CategoryChip from "../category/CategoryChip.vue";
import ItemStatus from "../item/ItemStatus.vue";
import LocationItemStatusIcon from "../location/LocationItemStatusIcon.vue";
import ItemId from "./ItemId.vue";
import CategoryInput from "../inputs/CategoryInput.vue";
import LocationInput from "../inputs/LocationInput.vue";
import SerialNumberInput from "../inputs/SerialNumberInput.vue";
import ItemTypeInput from "../inputs/ItemTypeInput.vue";
import ScanInput from "../inputs/ScanInput.vue";
import gqlFormData from "./formData.graphql";
import ContainerChip from "./ContainerChip.vue";
export default {
  name: "ItemBaseList",
  components: {
    ContainerChip,
    SerialNumberInput,
    LocationInput,
    CategoryInput,
    LocationItemStatusIcon,
    CategoryChip,
    NotesInput,
    NameInput,
    ItemList,
    ItemStatus,
    ItemId,
    ItemTypeInput,
    ScanInput,
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
          text: this.$t("plank.labels.status"),
          value: "locationStatus",
        },
        {
          text: this.$t("plank.labels.id_barcode"),
          value: "id",
        },
        {
          text: this.$t("plank.inventory.title"),
          value: "inventory.name",
        },
        {
          text: this.$t("plank.category.title"),
          value: "category.name",
        },
        {
          text: this.$t("plank.item_type.title"),
          value: "itemType.name",
        },
        { text: this.$t("plank.labels.name"), value: "name" },
        { text: this.$t("plank.labels.status"), value: "status" },
      ];
    },
  },
  data() {
    return {
      defaultItem: defaultItems.item,
      rules: rules,
      formData: {
        locations: [],
        categories: [],
        itemTypes: [],
        canCreate: false,
      },
    };
  },
  props: {
    itemStatuses: {
      type: Object,
      required: false,
      default: () => {},
    },
  },
};
</script>
