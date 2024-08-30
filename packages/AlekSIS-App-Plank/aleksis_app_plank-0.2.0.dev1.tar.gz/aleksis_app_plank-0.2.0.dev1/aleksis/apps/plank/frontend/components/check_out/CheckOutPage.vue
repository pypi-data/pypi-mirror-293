<template>
  <div>
    <v-stepper v-model="step" vertical>
      <v-stepper-step :complete="step > 1" :step="1">
        {{ $t("plank.check_out.process.select_borrowing_person_title") }}
      </v-stepper-step>
      <v-stepper-content :step="1">
        <v-form v-model="formValid">
          <inventory-input
            v-if="inventories"
            :inventories="inventories"
            v-model="inventory"
          />
          <person-input
            v-if="fullInventory"
            :persons="fullInventory.checkOutPersons"
            v-model="person"
          />
          <!-- FIXME Option to create persons -->
        </v-form>
      </v-stepper-content>

      <v-stepper-step :complete="step > 2" :step="2">
        {{ $t("plank.check_out.process.select_items_title") }}
      </v-stepper-step>
      <v-stepper-content :step="2">
        <v-row v-if="person">
          <v-col cols="12" md="6">
            <scan-input
              v-model="idOrBarcode"
              :hint="$t('plank.check_out.process.scan_hint')"
              ref="scanInput"
              persistent-hint
              @submit="addItem"
            />
            <v-btn color="primary" @click="addItem" class="mb-4">
              {{ $t("plank.check_out.process.add_item") }}
            </v-btn>
          </v-col>
          <v-col cols="12" md="6">
            <v-list>
              <template v-for="(item, index) in items">
                <v-list-item :key="item.id">
                  <v-list-item-content>
                    <v-list-item-title>
                      <item-label :item="item" :with-barcode="false" />
                      <v-chip
                        v-if="item?.byContainer"
                        label
                        small
                        outlined
                        color="purple"
                      >
                        {{ item.location.name }}
                      </v-chip>
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      <item-id :item="item" />
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn icon color="error" @click="removeItem(item)">
                      <v-icon>mdi-delete-outline</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
                <v-divider
                  v-if="index < items.length - 1"
                  :key="'divider' + item.id"
                />
              </template>
            </v-list>
          </v-col>
        </v-row>
        <v-btn color="success" large :disabled="!hasItems" @click="step = 3">
          {{ $t("plank.check_out.process.finish_scanning") }}
        </v-btn>
      </v-stepper-content>

      <v-stepper-step :step="3" :complete="step > 3">
        {{ $t("plank.check_out.process.confirm_check_out_title") }}
      </v-stepper-step>
      <v-stepper-content :step="3">
        <div v-if="!checkOutProcess">
          <v-form v-model="confirmFormValid">
            <check-in-until-input v-model="checkInUntil" />
            <check-out-condition-input
              v-if="fullInventory"
              :check-out-conditions="fullInventory.checkOutConditions"
              v-model="checkOutCondition"
            />
          </v-form>
          <ApolloMutation
            :mutation="require('./checkOut.graphql')"
            :variables="{
              input: {
                inventory,
                borrowingPerson: person,
                items: itemIds,
                checkOutCondition,
                checkInUntil: checkInUntil || null,
              },
            }"
            @done="checkOutDone"
          >
            <template #default="{ mutate, loading, error }">
              <div>
                <v-btn
                  color="success"
                  large
                  :disabled="!confirmFormValid || loading"
                  :loading="loading"
                  @click="mutate"
                >
                  <v-icon left>mdi-content-save-outline</v-icon>
                  {{ $t("plank.check_out.process.confirm_check_out") }}
                </v-btn>
                <v-btn color="error" large @click="abort" :disabled="loading">
                  <v-icon left>mdi-cancel</v-icon>
                  {{ $t("plank.check_out.process.cancel_check_out") }}
                </v-btn>
              </div>
            </template>
          </ApolloMutation>
        </div>
        <div v-else>
          <p class="text-h5">
            {{ $t("plank.check_out.process.finished_successfully") }}
          </p>
          <div>
            <v-btn
              color="primary"
              :href="checkOutProcess.checkOutForm"
              target="_blank"
              class="mr-2"
            >
              <v-icon left>mdi-file-pdf-box</v-icon>
              {{ $t("plank.check_out.process.download_form") }}
            </v-btn>
            <v-btn color="primary" @click="abort">
              <v-icon left>mdi-plus</v-icon>
              {{ $t("plank.check_out.process.another_check_out") }}
            </v-btn>
          </div>
        </div>
      </v-stepper-content>
    </v-stepper>
    <v-snackbar :color="snackbarColor" v-model="snackbar">
      <v-icon left v-if="snackbarColor === 'success'">
        mdi-check-circle-outline
      </v-icon>
      <v-icon left v-else> mdi-alert-circle-outline </v-icon>
      <span v-if="snackbarStatus === 'already_added'">
        {{ $t("plank.check_out.process.messages.already_added") }}
      </span>
      <span v-else-if="snackbarStatus === 'not_found'">
        {{ $t("plank.check_out.process.messages.not_found") }}
      </span>
      <span v-else-if="snackbarStatus === 'checked_out'">
        {{ $t("plank.check_out.process.messages.checked_out") }}
      </span>
      <span v-else-if="snackbarStatus === 'added'">
        {{ $t("plank.check_out.process.messages.added") }}
      </span>
      <v-btn text @click="snackbar = false"
        >{{ $t("plank.actions.close") }}
      </v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import PersonInput from "../inputs/PersonInput.vue";
import InventoryInput from "../inputs/InventoryInput.vue";
import ScanInput from "../inputs/ScanInput.vue";
import CheckOutConditionInput from "../inputs/CheckOutConditionInput.vue";
import CheckInUntilInput from "../inputs/CheckInUntilInput.vue";
import gqlItem from "./item.graphql";
import gqlInventories from "./inventories.graphql";
import ItemLabel from "../item/ItemLabel.vue";
import ItemId from "../item/ItemId.vue";

export default {
  name: "CheckOutPage",
  components: {
    CheckInUntilInput,
    CheckOutConditionInput,
    InventoryInput,
    PersonInput,
    ScanInput,
    ItemLabel,
    ItemId,
  },
  data() {
    return {
      step: 1,
      formValid: false,
      confirmFormValid: false,
      inventory: null,
      person: null,
      idOrBarcode: "",
      items: [],
      snackbar: false,
      snackbarStatus: "",
      checkOutCondition: null,
      checkInUntil: "",
      checkOutProcess: null,
    };
  },
  watch: {
    person(val) {
      if (val && this.step === 1) {
        this.step = 2;
      }
    },
    fullInventory(val) {
      console.log("Full inventory watch run", val, this.checkOutCondition);
      if (this.checkOutCondition === null && val) {
        const possibleCondition = this.fullInventory.checkOutConditions.find(
          (con) => con.default,
        );
        this.checkOutCondition = possibleCondition
          ? possibleCondition.id
          : null;
      }
    },
  },
  computed: {
    itemIds() {
      return this.items.map((item) => item.id);
    },
    fullInventory() {
      if (!this.inventories) {
        return;
      }
      return this.inventories.find(
        (inventory) => inventory.id === this.inventory,
      );
    },
    snackbarColor() {
      return this.snackbarStatus === "added" ? "success" : "error";
    },
    hasItems() {
      return this.items.length > 0;
    },
  },
  methods: {
    focusScanInput() {
      this.$refs.scanInput.focus();
    },
    clearScanInput() {
      this.idOrBarcode = "";
      this.focusScanInput();
    },
    addItem() {
      if (!this.idOrBarcode) {
        return;
      }
      this.$apollo
        .query({
          query: gqlItem,
          variables: {
            id: this.idOrBarcode,
          },
        })
        .then(({ data }) => {
          console.log(data);
          if (!data.item.item) {
            this.snackbarStatus = "not_found";
          } else if (this.itemIds.includes(data.item.item.id)) {
            this.snackbarStatus = "already_added";
          } else if (!data.item.item.isAvailable) {
            this.snackbarStatus = "checked_out";
          } else {
            this.items.push(data.item.item);
            this.snackbarStatus = "added";
          }

          for (const containedItem of data.item.containedItems) {
            if (
              !this.itemIds.includes(containedItem.id) &&
              containedItem.isAvailable
            ) {
              this.items.push({ ...containedItem, byContainer: true });
            }
          }
          this.snackbar = true;
          this.clearScanInput();
        })
        .catch((error) => {
          console.log(error);
          this.focusScanInput();
        });
    },
    removeItem(item) {
      this.items.splice(this.items.indexOf(item), 1);
      this.focusScanInput();
    },
    resetCheckOut() {
      this.items = [];
      this.checkOutCondition = null;
      this.checkInUntil = null;
      this.person = null;
    },
    abort() {
      this.resetCheckOut();
      this.checkOutProcess = null;
      this.step = 1;
    },
    checkOutDone({ data }) {
      this.resetCheckOut();
      this.checkOutProcess = data.checkOut.process;
    },
  },

  apollo: {
    inventories() {
      return {
        query: gqlInventories,
      };
    },
  },
};
</script>
