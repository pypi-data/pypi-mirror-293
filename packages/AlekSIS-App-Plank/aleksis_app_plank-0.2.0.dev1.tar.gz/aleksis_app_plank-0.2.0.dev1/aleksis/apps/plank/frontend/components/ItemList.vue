<template>
  <div>
    <v-snackbar :value="error !== null">
      {{ error }}
      <template #action="{ attrs }">
        <v-btn color="primary" text v-bind="attrs">
          {{ $t("plank.actions.close") }}
        </v-btn>
      </template>
    </v-snackbar>
    <v-data-table
      :headers="tableHeaders"
      :items="actualItems"
      :loading="$apollo.loading"
      :loading-text="$t('plank.loading')"
      :class="elevation ? 'elevation-1' : ''"
      :items-per-page="100"
    >
      <template #top>
        <v-toolbar flat>
          <v-toolbar-title
            ><slot name="title"
              ><div class="text-h4 my-1">
                {{ $t(`plank.${i18nKey}.title_plural`) }}
              </div></slot
            ></v-toolbar-title
          >
          <v-spacer></v-spacer>
          <v-btn
            color="green"
            class="white--text b-2"
            @click="createItem"
            v-if="showCreate"
          >
            {{ $t(`plank.${i18nKey}.actions.create`) }}
          </v-btn>
          <form-dialog
            :dialog="dialog"
            :edited-item="editedItem"
            :default-item="defaultItem"
            :edit-title="$t(`plank.${i18nKey}.actions.edit`)"
            :create-title="$t(`plank.${i18nKey}.actions.create`)"
            :close="close"
            :gql-mutation="gqlMutation"
            :gql-query="gqlQuery"
          >
            <template #fields="{ currentItem }">
              <slot name="fields" :current-item="currentItem"></slot>
            </template>
          </form-dialog>
          <delete-dialog
            :title="$t(`plank.${i18nKey}.delete_question`)"
            :gql-query="gqlQuery"
            :gql-mutation="gqlDeleteMutation"
            :close="closeDelete"
            :item-attribute="itemAttribute"
            :item="editedItem"
            :dialog="dialogDelete"
          ></delete-dialog>
        </v-toolbar>
      </template>

      <!-- Redirect slots for custom table content -->
      <template
        v-for="name in slotsToInclude"
        :slot="name"
        slot-scope="slotData"
      >
        <slot :name="name" v-bind="slotData" />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #item.actions="{ item }">
        <v-btn
          v-if="'canEdit' in item && item.canEdit"
          icon
          :title="$t(`plank.${i18nKey}.actions.edit`)"
          color="warning"
          @click="editItem(item)"
        >
          <v-icon> mdi-pencil-outline </v-icon>
        </v-btn>
        <v-btn
          v-if="'canDelete' in item && item.canDelete"
          icon
          :title="$t(`plank.${i18nKey}.actions.delete`)"
          color="error"
          @click="deleteItem(item)"
        >
          <v-icon> mdi-delete-outline </v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import FormDialog from "./FormDialog.vue";
import DeleteDialog from "./DeleteDialog.vue";

export default {
  name: "ItemList",
  components: { FormDialog, DeleteDialog },
  apollo: {
    items() {
      return {
        query: this.gqlQuery,
        error: function (error) {
          this.error = error;
        },
        skip() {
          return this.itemList !== null;
        },
      };
    },
  },
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      editedIndex: -1,
      editedItem: null,
      error: null,
      formValid: false,
    };
  },
  computed: {
    //(_, name) in $scopedSlots"        v-if="name.includes('item.')
    slotsToInclude() {
      return Object.keys(this.$scopedSlots).filter((name) =>
        name.includes("item."),
      );
    },
    tableHeaders() {
      return this.headers
        .concat([
          {
            text: this.$t("plank.actions.title"),
            value: "actions",
            sortable: false,
          },
        ])
        .filter((header) => this.hideColumns.indexOf(header.value) === -1);
    },
    actualItems() {
      if (this.itemList !== null) {
        return this.itemList;
      }
      return this.items;
    },
  },
  methods: {
    createItem() {
      this.dialog = true;
    },
    editItem(item) {
      this.editedIndex = this.actualItems.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      this.editedIndex = this.actualItems.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = null;
        this.editedIndex = -1;
      });
    },
    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = null;
        this.editedIndex = -1;
      });
    },
  },
  props: {
    i18nKey: {
      type: String,
      required: true,
    },
    gqlQuery: {
      type: Object,
      required: true,
    },
    gqlMutation: {
      type: Object,
      required: true,
    },
    gqlDeleteMutation: {
      type: Object,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
    itemAttribute: {
      type: String,
      required: true,
      default: "name",
    },
    defaultItem: {
      type: Object,
      required: true,
    },
    showCreate: {
      type: Boolean,
      required: false,
      default: true,
    },
    itemList: {
      type: Array,
      required: false,
      default: null,
    },
    elevation: {
      type: Boolean,
      required: false,
      default: true,
    },
    hideColumns: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
};
</script>
