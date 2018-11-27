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
      this.addQuery(this.query)
      this.$router.push(`/search/${this.query}`)
    },
    lucky: function() {
      this.incrementCount()
      this.addQuery(this.query)
      Query.query({"query": this.query}).then(function(result) {
        var temp = result.data.hits.hits
        var dict = [];
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
      let starttime = new Date().getTime();
	    localStorage.setItem("starttime", starttime);
      console.log("Restarted")
      console.log("Time is " + localStorage.getItem("starttime"));
      console.log("Number of Click Count: " + localStorage.getItem('clickCount')) 
      console.log("Queries: " + localStorage.getItem('queries'))  
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
    addQuery(query){
      let queries = localStorage.getItem('queries');
	    if (queries === null || queries == []) {
		    queries = "'"+ query + "', ";
		    //console.log("Query was empty");
	    }
      else {
	      queries = queries.concat("'" + query + "', ");
      }
	    localStorage.setItem('queries', queries);
      //console.log(localStorage.getItem('queries').toString());
    }
  }
}
</script>

<style scoped>
</style>
