import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    strict: true,
    state: {
        query: null
    },
    mutations: {
        setQuery (state, query) {
            state.query = query
        }
    },
    actions: {
        setQuery({commit}, query){
            commit('setQuery', query)
        }
    },
    getters: {
        getQuery: state => {
            return state.query
        }
    }
})