<template>
  <v-card>
    <v-card-text>
      <v-simple-table>
        <tbody>
          <slot></slot>
        </tbody>
      </v-simple-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "AttributesTable",
};
</script>
