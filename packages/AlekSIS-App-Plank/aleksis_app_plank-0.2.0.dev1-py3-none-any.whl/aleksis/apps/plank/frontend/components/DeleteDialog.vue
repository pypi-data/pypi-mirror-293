<template>
  <ApolloMutation
    v-if="dialogOpen"
    :mutation="gqlMutation"
    :variables="{ id: item.id }"
    :update="update"
    @done="close"
  >
    <template #default="{ mutate, loading, error }">
      <v-dialog v-model="dialogOpen" max-width="500px">
        <v-card>
          <v-card-title class="text-h5">
            {{ $t("plank.delete_question") }}
          </v-card-title>
          <v-card-text>
            <p class="text-body-1">{{ nameOfObject }}</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="close" :disabled="loading">{{
              $t("plank.actions.cancel")
            }}</v-btn>
            <v-btn
              color="red"
              text
              @click="mutate"
              :loading="loading"
              :disabled="loading"
            >
              {{ $t("plank.actions.delete") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-snackbar :value="error !== null">
        {{ error }}

        <template #action="{ attrs }">
          <v-btn color="primary" text v-bind="attrs" @click="error = null">
            {{ $t("plank.actions.close") }}
          </v-btn>
        </template>
      </v-snackbar>
    </template>
  </ApolloMutation>
</template>

<script>
export default {
  name: "DeleteDialog",
  data() {
    return {
      dialogOpen: this.dialog,
    };
  },
  computed: {
    nameOfObject() {
      return this.itemAttribute in this.item || {}
        ? this.item[this.itemAttribute]
        : this.item.toString();
    },
  },
  watch: {
    dialog(val) {
      this.dialogOpen = val;
    },
    dialogOpen(val) {
      if (!val) {
        this.close();
      }
    },
  },
  methods: {
    update(store) {
      if (!this.gqlQuery) {
        // There is no GraphQL query to update
        return;
      }

      // Read the data from cache for query
      const storedData = store.readQuery({ query: this.gqlQuery });

      if (!storedData) {
        // There are no data in the cache yet
        return;
      }

      const storedDataKey = Object.keys(storedData)[0];

      // Remove item from stored data
      const index = storedData[storedDataKey].findIndex(
        (m) => m.id === this.item.id,
      );
      storedData[storedDataKey].splice(index, 1);

      // Write data back to the cache
      store.writeQuery({ query: this.gqlQuery, storedData });
    },
  },
  props: {
    dialog: {
      type: Boolean,
      required: true,
    },
    item: {
      type: Object,
      required: false,
      default: null,
    },
    itemAttribute: {
      type: String,
      required: true,
      default: "name",
    },
    title: {
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
