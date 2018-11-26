import Api from '@/services/Api'

export default {
    query(q) {
        return Api().post('search', q)
    }
}