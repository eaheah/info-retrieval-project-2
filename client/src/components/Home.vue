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
          <v-btn color="blue" v-on:click="lucky()">
            I'm Feeling Lucky
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container>
      <v-layout row justify-center>
        <v-flex lg1 sm6 md3>
          <v-btn color="green" v-on:click="start()">
            Start
          </v-btn>
        </v-flex>
        <v-flex lg1 sm6 md3>
          <v-btn color="red" v-on:click="done()">
            Done
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
      this.incrementCount()
      this.addQuery(this.query, "")
      this.$router.push(`/search/${this.query}`)
    },
    lucky: function() {
      this.incrementCount()
      this.addQuery(this.query, "(L)")
      Query.query({"query": this.query}).then(function(result) {
        var temp = result.data.hits.hits
        if (temp.length >= 1){
          window.open(temp[0]._source.url, '_blank')
          //window.location.href = temp[0]._source.url
        }
        else {
          alert("0 Result Found. Unable to redirect to a new URL")
        }
      })
    },
    start: function(){
      localStorage.setItem('clickCount', 0);
      localStorage.setItem('queries', []);
      localStorage.setItem('queriesCount', 0);
      localStorage.setItem('luckyCount', 0)
      let starttime = new Date().getTime();
      localStorage.setItem("starttime", starttime);
      console.log("Restarted")
      console.log("Time is " + localStorage.getItem("starttime"));
      console.log("Number of Click Count: " + localStorage.getItem('clickCount')) 
      console.log("Queries: " + localStorage.getItem('queries'))
      console.log("Number of Queries (Normal + Lucky) Count: " + localStorage.getItem('queriesCount')) 
      console.log("Number of Lucky Count: " + localStorage.getItem('luckyCount'))  
    },
    done: function(){
      var endtime = new Date().getTime();
      var starttime = localStorage.getItem("starttime");
      var elapsedTime = 0;
      if (starttime !== null) {
        elapsedTime = (endtime - starttime) / 1000.0;
        console.log("Elapsed time: " + elapsedTime + " seconds");
      }
      console.log("Number of Click Count: " + localStorage.getItem('clickCount')) 
      console.log("Queries: " + localStorage.getItem('queries'))  
      console.log("Number of Queries (Normal + Lucky) Count: " + localStorage.getItem('queriesCount')) 
      console.log("Number of Lucky Count: " + localStorage.getItem('luckyCount')) 
    },
    incrementCount: function(){
      let count = localStorage.getItem('clickCount');
      if (count === null) {
        count = 0;
        //console.log("Count is null");
      }
      count = Math.floor(count) + 1;
      localStorage.setItem('clickCount', count);
      //console.log(localStorage.getItem('clickCount'))  
      },
    addQuery(query,mode){
      let queries = localStorage.getItem('queries');
      let queriesCount = localStorage.getItem('queriesCount');
      let luckyCount = localStorage.getItem('luckyCount');
      if (queries === null || queries == []) {
        queries = "'"+ query + mode + "', ";
        queriesCount = 0;
        luckyCount = 0;
        //console.log("Query was empty");
      }
      else {
        queries = queries.concat("'" + query + mode + "', ");
      }
      queriesCount = Math.floor(queriesCount) + 1;
      if (mode === "(L)") {
        luckyCount = Math.floor(luckyCount) + 1;
        localStorage.setItem('luckyCount', luckyCount)
      }
      localStorage.setItem('queries', queries);
      localStorage.setItem('queriesCount', queriesCount)
      //console.log(localStorage.getItem('queries').toString());
    }
  }
}
</script>

<style scoped>
</style>
