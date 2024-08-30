<template>
  <detail-page :id="$route.params.id" :gql-query="require('./detail.graphql')">
    <!-- FIXME EDIT DIALOGS -->
    <template #title="{ item }"
      >{{ $t("plank.inventory.overview.title") }}: {{ item.name }}</template
    >
    <template #content="{ item }">
      <v-card class="mb-2" v-if="item">
        <v-card-title class="text-h5">{{
          $t("plank.inventory.overview.inventory_title")
        }}</v-card-title>
        <v-card-text class="d-flex flex-wrap">
          <!-- FIXME Apply default filter -->
          <dashboard-button
            icon="mdi-label-multiple-outline"
            :to="{ name: 'plank.categories' }"
          >
            {{ $t("plank.category.title_plural") }}
          </dashboard-button>
          <dashboard-button
            icon="mdi-factory"
            :to="{ name: 'plank.manufacturers' }"
          >
            {{ $t("plank.manufacturer.title_plural") }}
          </dashboard-button>
          <dashboard-button
            icon="mdi-map-marker-multiple-outline"
            :to="{ name: 'plank.locations' }"
          >
            {{ $t("plank.location.title_plural") }}
          </dashboard-button>
          <dashboard-button
            icon="mdi-shape-outline"
            :to="{ name: 'plank.itemTypes' }"
          >
            {{ $t("plank.item_type.title_plural") }}
          </dashboard-button>
          <dashboard-button
            icon="mdi-inbox-multiple-outline"
            :to="{ name: 'plank.items' }"
          >
            {{ $t("plank.item.title_plural") }}
          </dashboard-button>
          <dashboard-button
            icon="mdi-import"
            :to="{ name: 'plank.inventoryForm' }"
          >
            {{ $t("plank.inventory.overview.inventory_process") }}
          </dashboard-button>
        </v-card-text>
      </v-card>
      <v-card class="mb-2" v-if="item">
        <v-card-title class="text-h5">{{
          $t("plank.inventory.overview.check_title")
        }}</v-card-title>
        <v-card-text>
          <!-- FIXME Apply default filter -->
          <!--          <dashboard-button icon="mdi-account-multiple-outline">-->
          <!--            {{ $t("plank.person.title_plural") }}-->
          <!--          </dashboard-button>-->
          <dashboard-button
            icon="mdi-cart-arrow-down"
            :to="{ name: 'plank.checkOut' }"
          >
            {{ $t("plank.check_out.title") }}
          </dashboard-button>
          <dashboard-button
            icon="mdi-cart-arrow-up"
            :to="{ name: 'plank.checkIn' }"
          >
            {{ $t("plank.check_in.title") }}
          </dashboard-button>
        </v-card-text>
      </v-card>
      <v-card v-if="item">
        <v-card-title class="text-h5">{{
          $t("plank.inventory.overview.status_title")
        }}</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="4" lg="2">
              <status-card
                :title="$t('plank.inventory.overview.status.inventoried_items')"
                :number="item.status.countItems"
              >
                <template #actions>
                  <v-btn text>
                    {{ $t("plank.inventory.overview.status.all_items") }}
                  </v-btn>
                </template>
              </status-card>
            </v-col>
            <v-col cols="12" md="4" lg="2">
              <status-card
                :title="$t('plank.inventory.overview.status.available_items')"
                :number="item.status.countAvailableItems"
                color="green"
              >
                <template #actions>
                  <v-btn text class="white--text">
                    {{ $t("plank.inventory.overview.status.all_items") }}
                  </v-btn>
                </template>
              </status-card>
            </v-col>
            <v-col cols="12" sm="12" md="4" lg="2">
              <status-card
                :title="$t('plank.inventory.overview.status.checked_out_items')"
                :number="item.status.countCheckedOutItems"
                color="orange"
              >
                <template #actions>
                  <v-btn text class="white--text">
                    {{
                      $t(
                        "plank.inventory.overview.status.all_check_out_processes",
                      )
                    }}
                  </v-btn>
                </template>
              </status-card>
            </v-col>
            <v-col cols="12" md="4" lg="2">
              <status-card
                :title="$t('plank.inventory.overview.status.not_in_time')"
                :number="item.status.countNotInTime"
                color="red"
              >
                <template #actions>
                  <v-btn text class="white--text">
                    {{
                      $t(
                        "plank.inventory.overview.status.all_check_out_processes",
                      )
                    }}
                  </v-btn>
                </template>
              </status-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </template>
  </detail-page>
</template>

<script>
import DashboardButton from "./DashboardButton.vue";
import StatusCard from "./StatusCard.vue";
import DetailPage from "../DetailPage.vue";

export default {
  name: "InventoryDetail",
  components: { DetailPage, StatusCard, DashboardButton },
};
</script>
