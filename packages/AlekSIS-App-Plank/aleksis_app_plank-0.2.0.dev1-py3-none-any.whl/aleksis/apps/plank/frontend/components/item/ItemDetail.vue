<template>
  <detail-page :id="$route.params.id" :gql-query="require('./detail.graphql')">
    <template #title="{ item }">{{ item.name }}</template>
    <template #content="{ item }">
      <v-row>
        <v-col cols="12" lg="6">
          <attributes-table>
            <barcode-row :data="item.barcode" />
            <inventory-row :data="item.inventory" />
            <is-location-row :data="item.isLocation" />
            <category-row :data="item.category" />
            <item-type-row :data="item.itemType" />
            <location-row :data="item.location" />
            <serial-number-row :data="item.serialNumber" />
            <item-status-row :data="item" />
            <last-time-seen-at-row :data="item.lastTimeSeenAt" />
            <notes-row :data="item.notes" />
          </attributes-table>
        </v-col>
        <v-col cols="12" lg="6">
          <check-out-history-table :items="item.checkedOutItems" />
        </v-col>
      </v-row>
    </template>
  </detail-page>
</template>

<script>
import DetailPage from "../DetailPage.vue";
import defaultIcons from "../../defaultIcons";
import AttributesTable from "../AttributesTable.vue";
import NotesRow from "../attributeRows/NotesRow.vue";
import InventoryRow from "../attributeRows/InventoryRow.vue";
import CategoryRow from "../attributeRows/CategoryRow.vue";
import ItemTypeRow from "../attributeRows/ItemTypeRow.vue";
import SerialNumberRow from "../attributeRows/SerialNumberRow.vue";
import LocationRow from "../attributeRows/LocationRow.vue";
import BarcodeRow from "../attributeRows/BarcodeRow.vue";
import LastTimeSeenAtRow from "../attributeRows/LastTimeSeenAtRow.vue";
import ItemStatusRow from "../attributeRows/ItemStatusRow.vue";
import CheckOutHistoryTable from "./CheckOutHistoryTable.vue";
import IsLocationRow from "../attributeRows/IsLocationRow.vue";

export default {
  name: "ItemDetail",
  components: {
    IsLocationRow,
    CheckOutHistoryTable,
    LastTimeSeenAtRow,
    BarcodeRow,
    LocationRow,
    SerialNumberRow,
    ItemTypeRow,
    CategoryRow,
    InventoryRow,
    NotesRow,
    DetailPage,
    AttributesTable,
    ItemStatusRow,
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
