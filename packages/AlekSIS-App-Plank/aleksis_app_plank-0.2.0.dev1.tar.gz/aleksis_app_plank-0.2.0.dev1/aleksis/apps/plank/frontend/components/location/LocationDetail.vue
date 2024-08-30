<template>
  <detail-page :id="$route.params.id" :gql-query="require('./detail.graphql')">
    <template #title="{ item }">{{ item.name }}</template>
    <template #content="{ item }">
      <v-row>
        <v-col cols="12" lg="6">
          <attributes-table class="mb-4">
            <parent-locations-row :data="item" />
            <notes-row :data="item.notes" />
            <item-row :data="item.item" />
          </attributes-table>
          <v-treeview
            item-children="children"
            item-key="id"
            item-label="name"
            :items="item.children"
            open-on-click
          >
            <template #prepend="{ prependItem, open }">
              <v-icon>
                {{ defaultIcons.location }}
              </v-icon>
            </template>
            <template #append="{ appendItem, open }">
              <v-btn
                right
                text
                color="primary"
                :to="{
                  name: 'plank.location',
                  params: { id: item.id },
                }"
              >
                {{ $t("plank.actions.show") }}
              </v-btn>
            </template>
          </v-treeview>
        </v-col>
        <v-col cols="12" lg="6">
          <ApolloMutation
            :mutation="require('./sortOrCheckMutation.graphql')"
            :variables="{
              locationId: $route.params.id,
              idOrBarcode: idOrBarcode,
              checkIn: checkIn,
            }"
            @error="handleError"
            @done="sortOrCheckDone"
            :update="updateCache"
          >
            <template #default="{ mutate, loading, error }">
              <v-card class="mb-4">
                <v-card-title
                  >{{ $t("plank.location.sort_or_check.title") }}
                </v-card-title>
                <v-card-text>
                  <scan-input
                    v-model="idOrBarcode"
                    @submit="mutate"
                    ref="scanInput"
                    :hint="$t('plank.location.sort_or_check.scan_hint')"
                    persistent-hint
                  ></scan-input>
                </v-card-text>
                <v-card-actions>
                  <v-btn
                    color="primary"
                    :disabled="loading || !sortValid"
                    :loading="loading"
                    @click="mutate"
                  >
                    {{ $t("plank.location.sort_or_check.action") }}
                  </v-btn>
                </v-card-actions>
              </v-card>

              <v-slide-y-transition>
                <v-card
                  v-if="Object.keys(itemStatuses).length > 0"
                  class="mb-4"
                >
                  <v-card-title
                    >{{ $t("plank.location.sort_or_check.ongoing_title") }}
                  </v-card-title>
                  <number-list-item
                    :data="item.itemsCount"
                    icon="mdi-map-marker-check-outline"
                  >
                    <template #title>
                      {{ $t("plank.location.sort_or_check.items_registered") }}
                    </template>
                  </number-list-item>
                  <v-divider />
                  <number-list-item
                    :data="item.itemsCount - inPlaceItemsCount"
                    icon="mdi-map-marker-remove-outline"
                    icon-color="error"
                  >
                    <template #title>
                      {{ $t("plank.location.sort_or_check.items_missing") }}
                    </template>
                  </number-list-item>
                  <v-divider />
                  <number-list-item
                    :data="movedItemsCount"
                    icon="mdi-map-marker-plus-outline"
                    icon-color="success"
                  >
                    <template #title>
                      {{ $t("plank.location.sort_or_check.items_moved") }}
                    </template>
                  </number-list-item>
                  <v-card-actions>
                    <v-btn
                      text
                      color="primary"
                      :href="`/app/plank/locations/${
                        $route.params.id
                      }/completeness?item_statuses=${JSON.stringify(
                        itemStatuses,
                      )}`"
                      target="_blank"
                    >
                      {{
                        $t(
                          "plank.location.sort_or_check.download_completeness_report",
                        )
                      }}
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-slide-y-transition>

              <v-dialog v-model="checkInDialog" max-width="500px">
                <v-card>
                  <v-card-title>
                    <v-icon left color="warning">mdi-alert-outline</v-icon>
                    {{
                      $t(
                        "plank.location.sort_or_check.currently_checked_out.title",
                      )
                    }}
                  </v-card-title>
                  <v-card-text>
                    <p>
                      {{
                        $t(
                          "plank.location.sort_or_check.currently_checked_out.text",
                        )
                      }}
                    </p>
                    <p>
                      <item-chip :item="checkInItem" />
                    </p>
                    <p>
                      {{
                        $t(
                          "plank.location.sort_or_check.currently_checked_out.question",
                        )
                      }}
                    </p>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer />
                    <v-btn color="primary" text @click="doNotCheckIn">
                      {{
                        $t(
                          "plank.location.sort_or_check.currently_checked_out.no",
                        )
                      }}
                    </v-btn>
                    <v-btn
                      color="primary"
                      text
                      @click="
                        doCheckIn();
                        mutate();
                      "
                    >
                      {{
                        $t(
                          "plank.location.sort_or_check.currently_checked_out.yes",
                        )
                      }}
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </template>
          </ApolloMutation>
        </v-col>

        <v-col cols="12">
          <item-base-list :item-list="item.items" :item-statuses="itemStatuses">
            <template #title>
              <v-toolbar-title>
                <v-icon left>{{ defaultIcons.items }}</v-icon>
                {{ $t("plank.item.title_plural") }}
              </v-toolbar-title>
            </template>
          </item-base-list>
        </v-col>
      </v-row>

      <v-snackbar
        v-for="(error, idx) in errors"
        :key="idx"
        color="error"
        :value="true"
      >
        <v-icon left>mdi-alert-circle-outline</v-icon>
        {{ error }}
      </v-snackbar>
      <v-snackbar color="success" v-model="snackbar">
        <v-icon left>mdi-check-circle-outline</v-icon>
        <span v-if="snackbarStatus === 'moved'">
          {{ $t("plank.location.sort_or_check.moved_success") }}
        </span>
        <span v-else-if="snackbarStatus === 'in_place'">
          {{ $t("plank.location.sort_or_check.in_place_success") }}
        </span>
        <v-btn text @click="snackbar = false"
          >{{ $t("plank.actions.close") }}
        </v-btn>
      </v-snackbar>
    </template>
  </detail-page>
</template>

<script>
import DetailPage from "../DetailPage.vue";
import defaultIcons from "../../defaultIcons";
import AttributesTable from "../AttributesTable.vue";
import NotesRow from "../attributeRows/NotesRow.vue";
import ItemBaseList from "../item/ItemBaseList.vue";
import ScanInput from "../inputs/ScanInput.vue";
import ItemChip from "../item/ItemChip.vue";
import NumberListItem from "./NumberListItem.vue";
import ParentLocationsRow from "../attributeRows/ParentLocationsRow.vue";
import gqlDetail from "./detail.graphql";
import ItemRow from "../attributeRows/ItemRow.vue";

export default {
  name: "LocationDetail",
  components: {
    ItemRow,
    ParentLocationsRow,
    NumberListItem,
    ItemChip,
    ScanInput,
    ItemBaseList,
    NotesRow,
    DetailPage,
    AttributesTable,
  },
  computed: {
    sortValid() {
      return this.idOrBarcode.length > 0;
    },
    inPlaceItemsCount() {
      let count = 0;
      for (let key in this.itemStatuses) {
        if (this.itemStatuses[key] === "in_place") {
          count++;
        }
      }
      return count;
    },
    movedItemsCount() {
      let count = 0;
      for (let key in this.itemStatuses) {
        if (this.itemStatuses[key] === "moved") {
          count++;
        }
      }
      return count;
    },
  },
  methods: {
    handleError(error) {
      if (error.networkError) {
        this.errors.push(error.networkError.toString());
      }
      if (error.graphQLErrors) {
        this.errors = this.errors.concat(
          error.graphQLErrors.map((x) => x.message),
        );
      }
      this.clearScanInput();
    },
    sortOrCheckDone(result) {
      const status = result.data.sortOrCheck.status;
      const item = result.data.sortOrCheck.item;
      if (status === "checked_out") {
        this.checkInDialog = true;
        this.checkInItem = item;
      } else {
        this.$set(this.itemStatuses, item.id, status);
        this.clearScanInput();
        this.checkIn = false;
        this.snackbarStatus = status;
        this.snackbarItem = item;
        this.snackbar = true;
      }
    },
    clearScanInput() {
      this.idOrBarcode = "";
      this.$refs.scanInput.focus();
    },
    doNotCheckIn() {
      this.checkInDialog = false;
      this.checkInItem = false;
      this.clearScanInput();
    },
    doCheckIn() {
      this.checkInDialog = false;
      this.checkInItem = false;
      this.checkIn = true;
    },
    updateCache(store, { data: { sortOrCheck } }) {
      const query = {
        query: gqlDetail,
        variables: {
          id: this.$route.params.id,
        },
      };

      if (sortOrCheck.status !== "moved") {
        return;
      }

      // Read the query from cache
      const data = store.readQuery(query);
      if (!data) {
        return;
      }

      // Mutate cache result
      data.item.items.push(sortOrCheck.item);

      // Write back to the cache
      store.writeQuery({
        ...query,
        data,
      });
    },
  },
  watch: {
    snackbar(val) {
      if (!val) {
        this.snackbarItem = null;
        this.snackbarStatus = "";
      }
    },
  },
  data() {
    return {
      defaultIcons: defaultIcons,
      idOrBarcode: "",
      checkIn: false,
      errors: [],
      checkInDialog: false,
      checkInItem: null,
      itemStatuses: {},
      snackbar: false,
      snackbarStatus: "",
      snackbarItem: null,
    };
  },
};
</script>
