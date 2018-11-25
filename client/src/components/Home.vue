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
        <v-flex lg1 sm6 md3>
          <v-btn flat icon color="blue" v-on:click="lucky()">
            I'm Feeling Lucky
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
import Query from '@/services/Query'

export default {
  data() {
    return {
      query: null,
    }
  },
  methods: {
    search: function() {
      this.$router.push(`/search/${this.query}`)
    },
    lucky: function() {
      console.log(this.query)
      
      Query.query({"query": this.query}).then(function(result) {
        var temp = result.data.hits.hits

        var dict = [];
        console.log(temp.length)
        if (temp.length >= 1){
          //Replace with first hit URL (temp[0.url~])
          window.location.href = "http://nba.com"
        }
      })
    }
  }
}
</script>

<style scoped>
</style>
