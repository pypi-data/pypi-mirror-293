<template>
  <div v-if="item">
    <!-- FIXME EDIT DIALOGS -->
    <h1 class="text-h3 mb-4">
      <slot name="title" :item="item"></slot>
      <span class="grey--text">#{{ item.id }}</span>
    </h1>
    <div class="mb-4">
      <v-btn color="primary" @click="$router.back()" class="mr-1">
        <v-icon left>mdi-chevron-left</v-icon>
        {{ $t("plank.actions.back") }}
      </v-btn>
      <v-btn color="warning" class="mr-1">
        <v-icon left>mdi-pencil</v-icon>
        {{ $t("plank.actions.edit") }}
      </v-btn>
      <v-btn color="error">
        <v-icon left>mdi-delete</v-icon>
        {{ $t("plank.actions.delete") }}
      </v-btn>
      <slot name="additional-actions" :item="item"></slot>
    </div>
    <slot name="content" :item="item"> </slot>
  </div>
</template>

<script>
export default {
  name: "DetailPage",
  components: {},
  apollo: {
    item() {
      return {
        query: this.gqlQuery,
        variables() {
          return {
            id: this.id,
          };
        },
      };
    },
  },
  data() {
    return {
      dialog: false,
      dialogDelete: false,
    };
  },
  props: {
    gqlQuery: {
      type: Object,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
  },
  methods: {
    editItem() {
      this.dialog = true;
    },
    deleteItem() {
      this.dialogDelete = true;
    },
    close() {
      this.dialog = false;
    },
    closeDelete() {
      this.dialogDelete = false;
    },
  },
};
</script>
