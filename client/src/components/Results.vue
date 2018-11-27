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
              <a v-bind:href="result.url" class="url" target=blank>
                {{result.url}}
              </a>
            </div>
            <div class="snip">
                <span v-html="result.snippet"></span>
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
  methods: {
    prepareRender(result) {
      var temp = result.data.hits.hits
        console.log(temp)
        var dict = [];
        var limit = Math.min(10, temp.length)
        console.log(limit)
        for (var i = 0; i < limit; i++) {
          var snippet = "No Highlight"
          if(temp[i].hasOwnProperty('highlight')){
            if(temp[i].highlight.hasOwnProperty('description')){
              snippet = this.bestSnippet(temp[i].highlight.description)
              //snippet = temp[i].highlight.description[index] + "..."
            }
            else if (temp[i].highlight.hasOwnProperty('site_text')){
              snippet = this.bestSnippet(temp[i].highlight.site_text)
             //snippet = temp[i].highlight.site_text[index] + "..."
            }
          }
          snippet = snippet.replace(/<em>/gm, "<strong>").replace(/<\/em>/gm, "</strong>");
          
          dict.push({
            title:  temp[i]._source.title,
            url:  temp[i]._source.url,
            snippet:  snippet
          })
        }
        return dict
    },
    bestSnippet(snippets){
      var max = -1;
      var index = 0;
      for(var i = 0; i < snippets.length; i++){
        var count = (snippets[i].match(/<em>/gm) || []).length
        if( count > max) {
          max = count
          index = i
        }
      }
      return snippets[index]
    }
  },
  watch: {
    query: function(newQuery, oldQuery) {
      let self = this
      var q = newQuery
      Query.query({"query": q}).then(function(result) {
        var dict = self.prepareRender(result)
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
    var results = (await Query.query({"query": q}))
    var dict = this.prepareRender(results)
    this.results = dict

    // eslint-disable-next-line
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
