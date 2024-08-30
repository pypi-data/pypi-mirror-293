<template>
  <div>
    <ApolloMutation
      :mutation="require('../item/mutation.graphql')"
      :variables="{ input: item }"
      @done="itemCreated"
    >
      <template #default="{ mutate, loading, error }">
        <v-slide-x-transition>
          <v-card v-if="createdItem" class="mb-4">
            <v-card-title>
              <v-icon left color="success">mdi-check-circle-outline</v-icon>
              {{ $t("plank.item.inventory_process.whats_next") }}
            </v-card-title>
            <v-card-text>
              <p class="text-body-1">
                {{ createdItem.name }} (#{{ createdItem.id }})
              </p>
              <v-btn color="primary" href="#form">
                {{ $t("plank.item.inventory_process.create_another_item") }}
              </v-btn>
              <v-btn
                color="primary"
                :to="{ name: 'plank.item', params: { id: createdItem.id } }"
                target="_blank"
              >
                {{ $t("plank.item.actions.show") }}
              </v-btn>
            </v-card-text>
          </v-card>
        </v-slide-x-transition>
        <v-form v-model="valid" id="form" ref="form">
          <v-card class="mb-4">
            <v-card-title>
              {{ $t("plank.item.inventory_process.barcode_name_title") }}
            </v-card-title>
            <v-card-text>
              <message-box type="primary">
                {{ $t("plank.item.inventory_process.barcode_hint") }}
              </message-box>
              <scan-input v-model="item.barcode" />
              <name-input v-model="item.name" />
            </v-card-text>
          </v-card>
          <v-card class="mb-4">
            <v-card-title>
              {{ $t("plank.item.inventory_process.inventory_title") }}
            </v-card-title>
            <v-card-text>
              <inventory-input
                v-model="item.inventory"
                :inventories="inventories"
              />
            </v-card-text>
          </v-card>
          <v-card v-if="item.inventory" class="mb-4">
            <v-card-title>
              {{ $t("plank.item.inventory_process.category_title") }}
              <v-spacer />
              <v-btn color="success" text @click="createCategoryDialog = true">
                {{ $t(`plank.category.actions.create`) }}
              </v-btn>
            </v-card-title>
            <v-card-text>
              <category-input
                v-model="item.category"
                :categories="categories"
              />
            </v-card-text>
          </v-card>
          <form-dialog
            :dialog="createCategoryDialog"
            :default-item="defaultItems.category"
            :edit-title="$t(`plank.category.actions.edit`)"
            :create-title="$t(`plank.category.actions.create`)"
            :close="close"
            :gql-mutation="require('../category/mutation.graphql')"
            :gql-query="require('./categories.graphql')"
            @objectSelected="categorySelected"
          >
            <template #fields="{ currentItem }">
              <!-- eslint-disable-next-line vue/valid-v-model -->
              <category-fields v-model="currentItem" :form-data="formData" />
            </template>
          </form-dialog>
          <v-card v-if="item.inventory" class="mb-4">
            <v-card-title>
              {{ $t("plank.item.inventory_process.item_type_title") }}
              <v-spacer />
              <v-btn color="success" text @click="createItemTypeDialog = true">
                {{ $t(`plank.item_type.actions.create`) }}
              </v-btn>
            </v-card-title>
            <v-card-text>
              <item-type-input
                v-model="item.itemType"
                :item-types="itemTypes"
              />
            </v-card-text>
          </v-card>
          <form-dialog
            :dialog="createItemTypeDialog"
            :default-item="defaultItems.itemType"
            :edit-title="$t(`plank.item_type.actions.edit`)"
            :create-title="$t(`plank.item_type.actions.create`)"
            :close="close"
            :gql-mutation="require('../item_type/mutation.graphql')"
            :gql-query="require('./itemTypes.graphql')"
            @objectSelected="itemTypeSelected"
          >
            <template #fields="{ currentItem }">
              <!-- eslint-disable-next-line vue/valid-v-model -->
              <item-type-fields v-model="currentItem" :form-data="formData" />
            </template>
          </form-dialog>
          <v-card v-if="item.inventory" class="mb-4">
            <v-card-title>
              {{ $t("plank.item.inventory_process.location_title") }}
            </v-card-title>
            <v-card-text>
              <location-input v-model="item.location" :locations="locations" />
            </v-card-text>
          </v-card>
          <v-card v-if="item.inventory" class="mb-4">
            <v-card-title>
              {{ $t("plank.item.inventory_process.meta_title") }}
            </v-card-title>
            <v-card-text>
              <serial-number-input v-model="item.serialNumber" />
              <notes-input v-model="item.notes" />
            </v-card-text>
          </v-card>
          <v-card v-if="item.inventory" class="mb-4">
            <v-card-text>
              <v-btn
                color="primary"
                :disabled="!valid || loading"
                @click="mutate"
                :loading="loading"
              >
                {{ $t("plank.item.actions.save") }}
              </v-btn>
            </v-card-text>
          </v-card>
        </v-form>
      </template>
    </ApolloMutation>
  </div>
</template>

<script>
import ScanInput from "../inputs/ScanInput.vue";
import NameInput from "../inputs/NameInput.vue";
import InventoryInput from "../inputs/InventoryInput.vue";
import CategoryInput from "../inputs/CategoryInput.vue";
import ItemTypeInput from "../inputs/ItemTypeInput.vue";
import LocationInput from "../inputs/LocationInput.vue";
import SerialNumberInput from "../inputs/SerialNumberInput.vue";
import defaultItems from "../../defaultItems";
import NotesInput from "../inputs/NotesInput.vue";
import FormDialog from "../FormDialog.vue";
import CategoryFields from "../category/CategoryFields.vue";
import ItemTypeFields from "../item_type/ItemTypeFields.vue";

import gqlInventories from "./inventories.graphql";
import gqlCategories from "./categories.graphql";
import gqlItemTypes from "./itemTypes.graphql";
import gqlLocations from "./locations.graphql";
import gqlFormData from "./formData.graphql";
export default {
  name: "InventoryForm",
  components: {
    ItemTypeFields,
    NotesInput,
    SerialNumberInput,
    ItemTypeInput,
    InventoryInput,
    NameInput,
    ScanInput,
    CategoryInput,
    LocationInput,
    FormDialog,
    CategoryFields,
  },
  apollo: {
    inventories() {
      return {
        query: gqlInventories,
      };
    },
    categories() {
      return {
        query: gqlCategories,
      };
    },
    itemTypes() {
      return {
        query: gqlItemTypes,
      };
    },
    locations() {
      return {
        query: gqlLocations,
      };
    },
    formData: {
      query: gqlFormData,
      result({ data }) {
        if (data) {
          this.formData = data;
        }
      },
    },
  },
  methods: {
    close() {
      this.createCategoryDialog = false;
      this.createItemTypeDialog = false;
    },
    itemCreated({ data }) {
      console.log(data);
      this.createdItem = data.item.item;
      this.item.name = "";
      this.item.barcode = "";
      this.item.notes = "";
      this.item.serialNumber = "";
      this.$refs.form.resetValidation();
    },
    categorySelected(category) {
      this.item.category = category.id;
    },
    itemTypeSelected(itemType) {
      this.item.itemType = itemType.id;
    },
  },
  watch: {
    createdItem(val) {
      if (val) {
        // Go to top of the page
        window.scrollTo(0, 0);
      }
    },
  },
  data() {
    return {
      item: defaultItems.item,
      valid: false,
      createCategoryDialog: false,
      createItemTypeDialog: false,
      defaultItems,
      formData: {
        inventories: [],
        categories: [],
        manufacturers: [],
      },
      createdItem: null,
    };
  },
};
</script>
