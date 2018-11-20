<template>
  <v-form>
    <v-container>
      <v-layout row justify-center>
        <v-flex lg4 sm6 md3>
          <v-text-field
            label="Solo"
            placeholder="Search"
            v-model="query"
            solo
          ></v-text-field>
        </v-flex>
        <v-flex lg1 sm6 md3>
          <v-btn flat icon color="blue" v-on:click="search()">
            <v-icon>search</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
export default {
  data() {
    return {
      query: null,
    }
  },
  methods: {
    search: function() {
      this.$router.push(`/search/${this.query}`)
    }
  }
}
</script>

<style scoped>
</style>
