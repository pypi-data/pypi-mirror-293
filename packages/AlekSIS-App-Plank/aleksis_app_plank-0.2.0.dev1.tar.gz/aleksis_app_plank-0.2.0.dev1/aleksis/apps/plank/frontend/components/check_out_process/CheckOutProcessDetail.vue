<template>
  <detail-page :id="$route.params.id" :gql-query="require('./detail.graphql')">
    <template #title="{ item }"></template>
    <template #additional-actions="{ item }">
      <v-btn color="primary" :href="item.checkOutForm" target="_blank">
        <v-icon left>mdi-file-pdf-box</v-icon>
        {{ $t("plank.check_out.process.download_form") }}
      </v-btn>
      <v-btn color="primary" :href="item.checkInForm" target="_blank">
        <v-icon left>mdi-file-pdf-box</v-icon>
        {{ $t("plank.check_in.process.download_form") }}
      </v-btn>
    </template>
    <template #content="{ item }">
      <v-row>
        <v-col cols="12" lg="6">
          <attributes-table>
            <inventory-row :data="item.inventory" />
            <lending-person-row :data="item.lendingPerson" />
            <borrowing-person-row :data="item.borrowingPerson" />
            <check-out-process-status-row :data="item" />
            <checked-out-at-row :data="item.checkedOutAt" />
            <check-in-until-row :data="item.checkInUntil" />
            <check-out-condition-row :data="item.condition" />
          </attributes-table>
        </v-col>
        <v-col cols="12" lg="6">
          <v-card>
            <v-card-title>{{
              $t("plank.check_out_process.checked_out_items")
            }}</v-card-title>
            <v-card-text>
              <v-list>
                <template
                  v-for="(checkedOutItem, index) in item.checkedOutItems"
                >
                  <v-list-item :key="checkedOutItem.id">
                    <v-list-item-content>
                      <v-list-item-title>
                        <item-label
                          :item="checkedOutItem.item"
                          :with-barcode="false"
                        />
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        <item-id :item="checkedOutItem.item" />
                      </v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                      <span v-if="checkedOutItem.checkedIn">
                        <v-chip color="green" text-color="white" label small>
                          {{ $t("plank.item.status.checked_in") }}
                        </v-chip>
                      </span>
                      <span v-else>
                        <v-chip
                          color="red"
                          class="mr-2"
                          text-color="white"
                          label
                          small
                        >
                          {{ $t("plank.item.status.checked_out") }}
                        </v-chip>
                        <v-btn icon color="green">
                          <v-icon>mdi-undo</v-icon>
                        </v-btn>
                      </span>
                    </v-list-item-action>
                  </v-list-item>
                  <v-divider
                    v-if="index < item.checkedOutItems.length - 1"
                    :key="'divider' + checkedOutItem.id"
                  />
                </template>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </detail-page>
</template>

<script>
import DetailPage from "../DetailPage.vue";
import defaultIcons from "../../defaultIcons";
import AttributesTable from "../AttributesTable.vue";
import InventoryRow from "../attributeRows/InventoryRow.vue";
import LendingPersonRow from "../attributeRows/LendingPersonRow.vue";
import CheckedOutAtRow from "../attributeRows/CheckedOutAtRow.vue";
import BorrowingPersonRow from "../attributeRows/BorrowingPersonRow.vue";
import CheckOutProcessStatusRow from "../attributeRows/CheckOutProcessStatusRow.vue";
import CheckInUntilRow from "../attributeRows/CheckInUntilRow.vue";
import CheckOutConditionRow from "../attributeRows/CheckOutConditionRow.vue";
import ItemLabel from "../item/ItemLabel.vue";
import ItemId from "../item/ItemId.vue";

export default {
  name: "CheckOutProcessDetail",
  components: {
    CheckOutConditionRow,
    CheckInUntilRow,
    CheckedOutAtRow,
    LendingPersonRow,
    InventoryRow,
    DetailPage,
    AttributesTable,
    BorrowingPersonRow,
    CheckOutProcessStatusRow,
    ItemLabel,
    ItemId,
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
