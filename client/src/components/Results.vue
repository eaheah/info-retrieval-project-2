<template>
  <v-container>
    <v-layout>
      <v-flex xs4 d-flex>
        <ul>
          <li v-for="(result) in results" :key="result.id">
            <div class="title"><font size="4">
              {{result.title}}
            </font>
            </div>
            <div>
              <a href="result.url" class="url">
                {{result.url}}
              </a>
            </div>
            <div class="snip">
              {{result.snippet}}
            </div>
          </li>
        </ul>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Query from '@/services/Query'
export default {
  data() {
    return {
      results: [{
        "title" : "This is just a test",
        "url" : "notArealURL.com",
        "snippet": "this would be something if this wasn't fake"
      }],
      query: this.$store.state.route.params.searchID
    };
  },

  watch: {
    query: function(newQuery, oldQuery) {
      let self = this
      console.log("Query Changed")
      var q = newQuery
      console.log(newQuery)
      console.log(oldQuery)
      Query.query({"query": q}).then(function(result) {
        var temp = result.data.hits.hits

        var dict = [];
        for (var i = 0; i < temp.length; i++) {
          var snippet = "No Highlight"
          if(temp[i].hasOwnProperty('highlight')){
            var snippet = temp[i].highlight.site_text[0] + "..."
            snippet = snippet.replace(/<\/?[^>]+(>|$)/g, "");
          }
          dict.push({
            title:  "(No Title Yet) Document " + (i+1),
            url:  "No URL Yet",
            snippet:  snippet
          })
        }
        console.log(self.results)
        console.log(dict)
        self.results = dict;
      })      
    },
    results(){
      console.log("Result Changed")
    }
  },

  beforeRouteUpdate(to, from, next) {
     this.query = to.params.searchID
     next();
  },

  async mounted() {
    var q = this.$store.state.route.params.searchID
    var results = (await Query.query({"query": q})).data.hits.hits 
    
    var dict = [];
    for (var i = 0; i < results.length; i++) {
      var snippet = "No Highlight"
      if(results[i].hasOwnProperty('highlight')){
        var snippet = results[i].highlight.site_text[0] + "..."
        snippet = snippet.replace(/<\/?[^>]+(>|$)/g, "");
      }
      dict.push({
        title:  "(No Title Yet) Document " + (i+1),
        url:  "No URL Yet",
        snippet:  snippet
      })
    }
    this.results = dict

    // eslint-disable-next-line
    console.log(results)
  }
};
</script>

<style scoped>
 li {
    margin-bottom: 20px
  }
  div {
    text-align: left
  }
  div.title {
    color: blue
  }
  a.url {
    color: green;
    white-space: nowrap;
    width: 570px;
    overflow: hidden;
    text-overflow: ellipsis
  }
  ul {
    list-style-type: none;
  }
</style>
