<template>
  <ApolloMutation
    :mutation="gqlMutation"
    :variables="{ input: currentItem }"
    :update="update"
    @done="onDone"
  >
    <template #default="{ mutate, loading, error }">
      <v-dialog v-model="dialogOpen" max-width="500px">
        <v-card :loading="loading">
          <v-card-title>
            <span class="text-h5">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text>
            <v-form v-model="formValid" ref="form">
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <form @submit.prevent="mutate">
                      <slot name="fields" :current-item="currentItem"></slot>
                    </form>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="closeDialog" :disabled="loading">
              {{ $t("plank.actions.cancel") }}
            </v-btn>
            <v-btn
              color="primary"
              text
              @click="mutate"
              :loading="loading"
              :disabled="!formValid || loading"
            >
              {{ $t("plank.actions.save") }}
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-snackbar :value="error !== null">
          {{ error }}

          <template #action="{ attrs }">
            <v-btn color="primary" text v-bind="attrs" @click="error = null">
              {{ $t("plank.actions.close") }}
            </v-btn>
          </template>
        </v-snackbar>
      </v-dialog>
    </template>
  </ApolloMutation>
</template>

<script>
export default {
  name: "FormDialog",
  data() {
    return {
      formValid: false,
      dialogOpen: this.dialog,
      currentItem: structuredClone(
        this.editedItem ? this.editedItem : this.defaultItem,
      ),
    };
  },
  computed: {
    edit() {
      return this.editedItem !== null;
    },
    formTitle() {
      return this.edit ? this.editTitle : this.createTitle;
    },
  },
  watch: {
    dialog(val) {
      this.dialogOpen = val;
    },
    dialogOpen(val) {
      if (!val) {
        this.closeDialog();
      }
    },
    editedItem(val) {
      if (val) {
        this.currentItem = structuredClone(val);
      } else {
        this.currentItem = structuredClone(this.defaultItem);
      }
    },
    currentItem() {
      const keys = Object.keys(this.defaultItem).concat(["id"]);
      for (let key in this.currentItem) {
        // Foreign key handling
        if (
          this.currentItem[key] &&
          typeof this.currentItem[key] === "object" &&
          "id" in this.currentItem[key]
        ) {
          this.currentItem[key] = this.currentItem[key]["id"];
        }

        // M2M handling
        if (
          this.currentItem[key] &&
          Array.isArray(this.currentItem[key]) &&
          this.currentItem[key].length > 0 &&
          typeof this.currentItem[key][0] === "object" &&
          "id" in this.currentItem[key][0]
        ) {
          this.currentItem[key] = this.currentItem[key].map(
            (item) => item["id"],
          );
        }

        // These items can't be saved.
        if (keys.indexOf(key) === -1) {
          delete this.currentItem[key];
        }
      }
    },
  },
  methods: {
    update(store, { data }) {
      if (!this.gqlQuery || this.edit) {
        // There is no GraphQL query to update
        return;
      }
      const dataKey = Object.keys(data)[0];
      const dataItem = data[dataKey][dataKey];

      // Read the data from cache for this query
      const storedData = store.readQuery({ query: this.gqlQuery });

      if (!storedData) {
        // There are no data in the cache yet
        return;
      }

      const storedDataKey = Object.keys(storedData)[0];

      // Add the item to the query
      storedData[storedDataKey].push(dataItem);

      // Write data back to the cache
      store.writeQuery({ query: this.gqlQuery, storedData });
    },
    onDone(result) {
      if (result && result.data) {
        const dataKey = Object.keys(result.data)[0];
        const secondDataKey = Object.keys(result.data[dataKey])[0];
        this.$emit("objectSelected", result.data[dataKey][secondDataKey]);
      }
      this.closeDialog();
    },
    closeDialog() {
      this.currentItem = structuredClone(this.defaultItem);
      this.$refs.form.resetValidation();
      this.close();
    },
  },
  props: {
    dialog: {
      type: Boolean,
      required: true,
    },
    editedItem: {
      type: Object,
      required: false,
      default: null,
    },
    defaultItem: {
      type: Object,
      required: true,
    },
    editTitle: {
      type: String,
      required: true,
    },
    createTitle: {
      type: String,
      required: true,
    },
    close: {
      type: Function,
      required: true,
    },
    gqlMutation: {
      type: Object,
      required: true,
    },
    gqlQuery: {
      type: Object,
      required: false,
      default: null,
    },
  },
};
</script>
